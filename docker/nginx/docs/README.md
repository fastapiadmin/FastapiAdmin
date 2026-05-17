# 官网静态文件目录

请将官网构建产物( dist 文件夹)放置于此目录。

例如:
```bash
cp -r 你的docs项目/dist ./
```

最终目录结构应为:
```
docker/nginx/docs/
└── dist/
    ├── index.html
    ├── assets/
    └── ...
```
