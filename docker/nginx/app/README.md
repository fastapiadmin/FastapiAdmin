# 小程序静态文件目录

请将小程序 H5 构建产物( dist 文件夹)放置于此目录。

小程序 UniApp 的 H5 构建输出结构为 `dist/build/h5/`。

最终目录结构应为:
```
docker/nginx/app/
└── dist/
    └── build/
        └── h5/
            ├── index.html
            ├── static/
            └── ...
```
