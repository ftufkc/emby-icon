# emby-icon
## 使用
引用地址：https://github.com/ftufkc/emby-icon/raw/refs/heads/main/emby-icon.json

## 开发
### 1. 安装 Pillow
```shell
pip install pillow
```

### 2. 准备字体（示例用思源黑体粗体）
```shell
wget https://github.com/IU-Libraries-Joint-Development/pumpkin/raw/refs/heads/master/app/assets/fonts/NotoSansCJK/NotoSansCJKtc-Bold.ttf

```

### 3. 运行脚本
```shell
python icon_maker.py ./input_icons ./output_icons "我的emby" --radius 24 --font SourceHanSerifSC-Heavy.otf
```
