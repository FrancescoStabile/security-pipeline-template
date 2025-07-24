#!/usr/bin/env python3
"""
Simple Security Report Generator
Consolidates security scan results into a unified report
Uses only standard library - no external dependencies required
"""

import json
import os
import argparse
from pathlib import Path
from datetime import datetime

class SimpleSecurityReportGenerator:
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize counters
        self.vulnerabilities = []
        self.summary = {
            'scan_date': datetime.now().isoformat(),
            'total_issues': 0,
            'sast': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
            'sca': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
            'secrets': {'found': 0},
            'container': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
            'security_score': 100
        }
    
    def process_npm_audit(self, file_path: Path):
        """Process npm audit results"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            for vuln_id, vuln_data in data.get('vulnerabilities', {}).items():
                severity = vuln_data.get('severity', 'low').lower()
                if severity not in ['critical', 'high', 'medium', 'low']:
                    severity = 'low'
                
                vulnerability = {
                    'tool': 'npm audit',
                    'type': 'SCA',
                    'rule_id': vuln_id,
                    'severity': severity,
                    'message': vuln_data.get('title', 'Dependency vulnerability'),
                    'package': vuln_data.get('name', 'unknown'),
                    'file': 'package.json'
                }
                self.vulnerabilities.append(vulnerability)
                self.summary['sca'][severity] += 1
                
        except Exception as e:
            print(f"⚠️ Error processing npm audit: {e}")
    
    def process_osv_results(self, file_path: Path):
        """Process OSV Scanner results"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            for result in data.get('results', []):
                for package in result.get('packages', []):
                    for vuln in package.get('vulnerabilities', []):
                        # Map OSV severity to our scale
                        severity = 'medium'  # Default for OSV findings
                        
                        vulnerability = {
                            'tool': 'OSV Scanner',
                            'type': 'SCA',
                            'rule_id': vuln.get('id', 'unknown'),
                            'severity': severity,
                            'message': vuln.get('summary', 'Vulnerability found'),
                            'package': package.get('package', {}).get('name', 'unknown'),
                            'file': result.get('source', {}).get('path', '')
                        }
                        self.vulnerabilities.append(vulnerability)
                        self.summary['sca'][severity] += 1
                        
        except Exception as e:
            print(f"⚠️ Error processing OSV results: {e}")
    
    def process_eslint_results(self, file_path: Path):
        """Process ESLint results"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            for result in data.get('results', []):
                for message in result.get('messages', []):
                    # Map ESLint severity
                    severity_map = {2: 'high', 1: 'medium', 0: 'low'}
                    severity = severity_map.get(message.get('severity', 0), 'low')
                    
                    vulnerability = {
                        'tool': 'ESLint',
                        'type': 'SAST',
                        'rule_id': message.get('ruleId', 'unknown'),
                        'severity': severity,
                        'message': message.get('message', ''),
                        'file': result.get('filePath', ''),
                        'line': message.get('line', 0)
                    }
                    self.vulnerabilities.append(vulnerability)
                    self.summary['sast'][severity] += 1
                    
        except Exception as e:
            print(f"⚠️ Error processing ESLint results: {e}")
    
    def process_trufflehog_results(self, file_path: Path):
        """Process TruffleHog results"""
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        result = json.loads(line)
                        vulnerability = {
                            'tool': 'TruffleHog',
                            'type': 'Secrets',
                            'rule_id': result.get('DetectorName', 'secret-detected'),
                            'severity': 'critical',
                            'message': f"Secret detected: {result.get('DetectorName', 'Unknown')}",
                            'file': result.get('SourceMetadata', {}).get('Data', {}).get('Git', {}).get('file', ''),
                            'line': result.get('SourceMetadata', {}).get('Data', {}).get('Git', {}).get('line', 0)
                        }
                        self.vulnerabilities.append(vulnerability)
                        self.summary['secrets']['found'] += 1
                    except json.JSONDecodeError:
                        continue
                        
        except Exception as e:
            print(f"⚠️ Error processing TruffleHog results: {e}")
    
    def process_trivy_results(self, file_path: Path):
        """Process Trivy container scan results"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            for result in data.get('Results', []):
                for vuln in result.get('Vulnerabilities', []):
                    severity = vuln.get('Severity', 'UNKNOWN').lower()
                    if severity not in ['critical', 'high', 'medium', 'low']:
                        severity = 'medium'
                    
                    vulnerability = {
                        'tool': 'Trivy',
                        'type': 'Container',
                        'rule_id': vuln.get('VulnerabilityID', 'unknown'),
                        'severity': severity,
                        'message': vuln.get('Title', 'Container vulnerability'),
                        'package': vuln.get('PkgName', ''),
                        'file': 'Dockerfile'
                    }
                    self.vulnerabilities.append(vulnerability)
                    self.summary['container'][severity] += 1
                    
        except Exception as e:
            print(f"⚠️ Error processing Trivy results: {e}")
    
    def process_hadolint_results(self, file_path: Path):
        """Process Hadolint Dockerfile lint results"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            for result in data:
                # Map Hadolint levels to our severity
                level_map = {'error': 'high', 'warning': 'medium', 'info': 'low'}
                severity = level_map.get(result.get('level', 'info'), 'low')
                
                vulnerability = {
                    'tool': 'Hadolint',
                    'type': 'Container',
                    'rule_id': result.get('code', 'dockerfile-issue'),
                    'severity': severity,
                    'message': result.get('message', 'Dockerfile issue'),
                    'file': 'Dockerfile',
                    'line': result.get('line', 0)
                }
                self.vulnerabilities.append(vulnerability)
                self.summary['container'][severity] += 1
                
        except Exception as e:
            print(f"⚠️ Error processing Hadolint results: {e}")
    
    def calculate_security_score(self):
        """Calculate overall security score"""
        base_score = 100
        
        # Define penalty weights
        penalties = {
            'critical': 20,
            'high': 10,
            'medium': 5,
            'low': 1
        }
        
        total_penalty = 0
        
        # Calculate penalties for each category
        for category in ['sast', 'sca', 'container']:
            for severity, count in self.summary[category].items():
                total_penalty += count * penalties.get(severity, 0)
        
        # Extra penalty for secrets
        total_penalty += self.summary['secrets']['found'] * 25
        
        # Calculate final score
        score = max(0, base_score - total_penalty)
        self.summary['security_score'] = score
    
    def generate_html_report(self):
        """Generate HTML report"""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Scan Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .metric {{ background: #ecf0f1; padding: 15px; border-radius: 5px; text-align: center; }}
        .critical {{ border-left: 5px solid #e74c3c; }}
        .high {{ border-left: 5px solid #f39c12; }}
        .medium {{ border-left: 5px solid #f1c40f; }}
        .low {{ border-left: 5px solid #27ae60; }}
        .score {{ font-size: 2em; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #34495e; color: white; }}
        .severity-critical {{ background-color: #ffebee; }}
        .severity-high {{ background-color: #fff3e0; }}
        .severity-medium {{ background-color: #fffde7; }}
        .severity-low {{ background-color: #f1f8e9; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Security Scan Report</h1>
            <p>Generated on: {self.summary['scan_date']}</p>
            <div class="score">Security Score: {self.summary['security_score']}/100</div>
        </div>
        
        <div class="summary">
            <div class="metric critical">
                <h3>Critical Issues</h3>
                <h2>{sum(cat.get('critical', 0) for cat in [self.summary['sast'], self.summary['sca'], self.summary['container']]) + (1 if self.summary['secrets']['found'] > 0 else 0)}</h2>
            </div>
            <div class="metric high">
                <h3>High Issues</h3>
                <h2>{sum(cat.get('high', 0) for cat in [self.summary['sast'], self.summary['sca'], self.summary['container']])}</h2>
            </div>
            <div class="metric medium">
                <h3>Medium Issues</h3>
                <h2>{sum(cat.get('medium', 0) for cat in [self.summary['sast'], self.summary['sca'], self.summary['container']])}</h2>
            </div>
            <div class="metric low">
                <h3>Low Issues</h3>
                <h2>{sum(cat.get('low', 0) for cat in [self.summary['sast'], self.summary['sca'], self.summary['container']])}</h2>
            </div>
        </div>
        
        <h2>Detailed Findings</h2>
        <table>
            <thead>
                <tr>
                    <th>Tool</th>
                    <th>Type</th>
                    <th>Severity</th>
                    <th>Rule ID</th>
                    <th>Message</th>
                    <th>File</th>
                    <th>Line</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Add vulnerability rows
        for vuln in self.vulnerabilities[:50]:  # Limit to first 50 for readability
            html_content += f"""
                <tr class="severity-{vuln['severity']}">
                    <td>{vuln['tool']}</td>
                    <td>{vuln['type']}</td>
                    <td>{vuln['severity'].title()}</td>
                    <td>{vuln['rule_id']}</td>
                    <td>{vuln['message'][:100]}{'...' if len(vuln['message']) > 100 else ''}</td>
                    <td>{vuln.get('file', '')}</td>
                    <td>{vuln.get('line', '')}</td>
                </tr>
"""
        
        html_content += """
            </tbody>
        </table>
        
        <div style="margin-top: 40px; padding: 20px; background: #ecf0f1; border-radius: 5px;">
            <h3>📊 Summary by Category</h3>
            <ul>
                <li><strong>SAST (Static Analysis):</strong> Code quality and security issues</li>
                <li><strong>SCA (Dependency Analysis):</strong> Known vulnerabilities in dependencies</li>
                <li><strong>Secrets Detection:</strong> Exposed credentials and secrets</li>
                <li><strong>Container Security:</strong> Docker image and configuration issues</li>
            </ul>
        </div>
    </div>
</body>
</html>"""
        
        with open(self.output_dir / 'security-report.html', 'w') as f:
            f.write(html_content)
    
    def generate_sarif_output(self):
        """Generate SARIF output for GitHub Security tab"""
        sarif_template = {
            "version": "2.1.0",
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "runs": [{
                "tool": {
                    "driver": {
                        "name": "Security Pipeline Aggregator",
                        "version": "1.0.0"
                    }
                },
                "results": []
            }]
        }
        
        for vuln in self.vulnerabilities:
            # Map severity to SARIF levels
            level_map = {
                'critical': 'error',
                'high': 'error',
                'medium': 'warning',
                'low': 'note'
            }
            
            result = {
                "ruleId": vuln['rule_id'],
                "message": {"text": vuln['message']},
                "level": level_map.get(vuln['severity'], 'note'),
                "locations": [{
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": vuln.get('file', 'unknown')
                        },
                        "region": {
                            "startLine": max(1, vuln.get('line', 1))
                        }
                    }
                }]
            }
            sarif_template["runs"][0]["results"].append(result)
        
        with open(self.output_dir / 'consolidated.sarif', 'w') as f:
            json.dump(sarif_template, f, indent=2)
    
    def run(self):
        """Run the report generation process"""
        print("🔍 Starting security report generation...")
        
        # Process all available report files
        for file_path in self.input_dir.rglob('*.json'):
            filename = file_path.name.lower()
            
            try:
                if 'npm-audit' in filename:
                    self.process_npm_audit(file_path)
                elif 'osv-report' in filename:
                    self.process_osv_results(file_path)
                elif 'eslint' in filename:
                    self.process_eslint_results(file_path)
                elif 'trufflehog' in filename:
                    self.process_trufflehog_results(file_path)
                elif 'trivy' in filename:
                    self.process_trivy_results(file_path)
                elif 'hadolint' in filename:
                    self.process_hadolint_results(file_path)
                    
            except Exception as e:
                print(f"⚠️ Error processing {file_path}: {e}")
        
        # Calculate final metrics
        self.summary['total_issues'] = len(self.vulnerabilities)
        self.calculate_security_score()
        
        # Generate outputs
        print("📊 Generating reports...")
        
        # JSON Summary
        with open(self.output_dir / 'summary.json', 'w') as f:
            json.dump(self.summary, f, indent=2)
        
        # Full JSON Report
        full_report = {
            'summary': self.summary,
            'vulnerabilities': self.vulnerabilities
        }
        with open(self.output_dir / 'full-report.json', 'w') as f:
            json.dump(full_report, f, indent=2)
        
        # HTML Report
        self.generate_html_report()
        
        # SARIF Output
        self.generate_sarif_output()
        
        print(f"✅ Report generation complete!")
        print(f"📁 Reports saved to: {self.output_dir}")
        print(f"🛡️ Security Score: {self.summary['security_score']}/100")
        print(f"🔍 Total Issues Found: {self.summary['total_issues']}")

def main():
    parser = argparse.ArgumentParser(description='Generate security scan report')
    parser.add_argument('--input-dir', required=True, help='Input directory with scan results')
    parser.add_argument('--output-dir', required=True, help='Output directory for reports')
    
    args = parser.parse_args()
    
    generator = SimpleSecurityReportGenerator(args.input_dir, args.output_dir)
    generator.run()

if __name__ == '__main__':
    main()
