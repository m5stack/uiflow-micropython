# UIFLOW2 API Documentation

# Building Documentation

## 安装环境

```shell
pip3 install -r requirements.txt
```

## 编译

```shell
sphinx-build -b gettext ./en build/gettext
sphinx-intl update -p ./build/gettext -l zh_CN
sphinx-build -b html -D language=zh_CN ./en/ build/html/zh_CN # 简体中文
sphinx-build -b html -D language=en ./en/ build/html/en # English
```

## 预览

打开 build/html/zh_CN/index.html，即可在浏览器上预览。
