const { spawn } = require('child_process');

const text = process.argv[2];
if (!text) {
  console.error('Usage: node bridge.js <thai text>');
  process.exit(1);
}

const py = spawn('python3', ['thai_analysis.py', text]);
py.stdout.on('data', (data) => {
  process.stdout.write(data);
});
py.stderr.on('data', (data) => {
  process.stderr.write(data);
});