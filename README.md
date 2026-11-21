# evren-yolo26-yolo11-training-suite

[![CI](https://github.com/kenantabak/evren-yolo26-yolo11-training-suite/actions/workflows/ci.yml/badge.svg)](https://github.com/kenantabak/evren-yolo26-yolo11-training-suite/actions/workflows/ci.yml)

Farklı görsel alanlara (trafik levhaları, İHA/hava görüntüleri, tıbbi radyoloji, endüstriyel İSG/KKD) özel **`YOLO26` & `YOLO11` YAML eğitim profilleri** ve eğitim öncesi veri seti doğrulama (`preflight`) kütüphanesi.

## Neden Veriye Özel YAML Profilleri?

- **Trafik Levhaları & Metin/Rakamlar (`configs/traffic_signs.yaml`):** `fliplr=0.0`, `flipud=0.0`, `degrees=0.0` ayarlarıyla hız sınırı rakamlarının ve sola/sağa dönüş oklarının aynalanarak yanlış etikete dönüşmesini engeller.
- **İHA / Küçük Hedefler (`configs/uav_aerial.yaml`):** Küçük araçların/dronların kaybolmaması için `erasing=0.0`, tepe açısı çeşitliliği için `flipud=0.5`, `degrees=15.0` kullanır.
- **Tıbbi Radyoloji (`configs/medical_grayscale.yaml`):** Röntgen ve BT dokusunu bozmamak için `hsv_h=0.0`, `hsv_s=0.0` uygular.
- **Eğitim Öncesi (`src/training_suite/preflight.py`):** Uzun dosya adlarını (`>190` bayt), büyük/küçük harf sınıf çakışmalarını ve doğrulama (`val`) kümesinde `0` kutulu kalan sınıfları yakalar.

## Kurulum ve Testler

```bash
git clone https://github.com/kenantabak/evren-yolo26-yolo11-training-suite.git
cd evren-yolo26-yolo11-training-suite
pip install -e .
pytest -v
```
