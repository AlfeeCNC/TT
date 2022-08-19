# 環境
本專案以 Python Django 框架撰寫，建議使用 virtualenv 來架設虛擬環境。

當環境準備完成，進入虛擬環境，並輸入
```
pip3 install -r requirements.txt
```
就能安裝本專案相關的所有依賴套件。

> 注意！其中一個套件：`django-formtools` 必須手動安裝，輸入`pip3 install django-formtools`來完成安裝。

所有套件安裝完畢後，輸入
```
python manage.py runserver 0.0.0.0:8000
```
以執行專案


# Environment
This project is built with Python Django framework, so we recommend using virtualenv to set up the environment.

While environment is ready, run

```
pip3 install -r requirements.txt
```
to install all the dependency packages used in this project.
> WARNING!! A package called `django-formtools` need to install manually, run `pip3 install django-formtools` to install it.

then run
```
python manage.py runserver 0.0.0.0:8000
```
to start the project.
