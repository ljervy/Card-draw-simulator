const fs = require("fs");

const directories = [
  "./build",
  "./dist",
];

directories.forEach((dir) => {
  if (fs.existsSync(dir)) {
    console.log(`Removing ${dir}`);
    fs.rmSync(dir, { recursive: true});
    console.log(`Removed ${dir}`);
  } else {
    console.log(`${dir} not found`);
  }
});
