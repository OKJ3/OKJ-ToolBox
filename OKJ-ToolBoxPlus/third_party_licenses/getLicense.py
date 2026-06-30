import os
import requests
import tarfile
import io
import win32api

OUTPUT_DIR = "third_party_licenses"
os.makedirs(OUTPUT_DIR, exist_ok=True)

LICENSE_URLS = {
    "numpy": "https://raw.githubusercontent.com/numpy/numpy/main/LICENSE.txt",
    "pandas": "https://raw.githubusercontent.com/pandas-dev/pandas/main/LICENSE",
    "scipy": "https://raw.githubusercontent.com/scipy/scipy/main/LICENSE.txt",
    "matplotlib": "https://raw.githubusercontent.com/matplotlib/matplotlib/main/LICENSE/LICENSE",
    "pillow": "https://raw.githubusercontent.com/python-pillow/Pillow/main/LICENSE",
    "wxPython": "https://raw.githubusercontent.com/wxWidgets/wxWidgets/master/docs/licence.txt",

    # pywin32 は GitHub ではなく PyPI から取得する
    "pywin32": "https://files.pythonhosted.org/packages/source/p/pywin32/pywin32-306.tar.gz",
}

def download_license(name, url):
    print(f"Downloading {name} license...")

    try:
        if name != "pywin32":
            # 通常の GitHub RAW 取得
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            filepath = os.path.join(OUTPUT_DIR, f"{name}_LICENSE.txt")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(response.text)

            print(f"✔ Saved: {filepath}")

        else:
            # PyPI の tar.gz を取得して LICENSE.txt を抽出
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            tar_bytes = io.BytesIO(response.content)
            with tarfile.open(fileobj=tar_bytes, mode="r:gz") as tar:
                for member in tar.getmembers():
                    if member.name.endswith("LICENSE.txt"):
                        license_file = tar.extractfile(member)
                        text = license_file.read().decode("utf-8")

                        filepath = os.path.join(OUTPUT_DIR, f"{name}_LICENSE.txt")
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(text)

                        print(f"✔ Saved: {filepath}")
                        return

            print(f"✘ LICENSE.txt not found inside pywin32 package")
            print(win32api.__file__)

    except Exception as e:
        print(f"✘ Failed to download {name}: {e}")

def main():
    print("=== Downloading third-party licenses ===")
    for name, url in LICENSE_URLS.items():
        download_license(name, url)
    print("=== Done ===")

if __name__ == "__main__":
    main()
