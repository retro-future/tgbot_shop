# Telegram shop bot with django admin 


How to set up the project:
* Copy the project using:
```
  https://github.com/retro-future/tgbot_shop
```

* Go to folder:
```bash
  cd tgbot_shop 
```
---
>Rename .env.dist file to .env and enter your credentials

> You can get BOT_TOKEN and PROVIDER_TOKEN(Payment token) in Telegram @BotFather

---

* Run the command:
```bash
  docker-compose up 
```
![](https://telegra.ph/file/e32b7b15a4ee03b938697.png)

* This will start-up Bot and Django, once you start you'll get the notification in your bot like:
<br/>

![](https://telegra.ph/file/d0377e40fd1263a50389d.png)

---

* After you have to execute commands consistently:
```bash
  docker exec -it <container_id_or_name> python manage.py createsuperuser
```

```bash
  docker exec -it <container_id_or_name> python manage.py createsuperuser
```
* in order to create superuser to access django admin panel:
<br/>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![](https://telegra.ph/file/2347b88c6ff7b4ef2fa2a.png)

---

* The admin dashboard will be available at
```bash
  http://127.0.0.1:8000/
```
___

* Admin Dashboard

<br/>

 ![](https://telegra.ph/file/371fa9275f855df6f2675.png)

### Click on "Category" section and add one or more category,The category you've created will be shown on bot only if you're add <span style="color:red">"Subcategory"</span> to it

---

Once You've added "Category" "Subcategory" and "Product" you can see it in your bot 

![](https://telegra.ph/file/56651db3d2cda6d7786ef.png)

Click on category you've created e.g. and you'll see your subcatecory:

![](https://telegra.ph/file/3c9d1aa2adaf97fb23e7f.png)

After You clicked on subcategory you turn to inline-mode and list of your products will be displayed:

![](https://telegra.ph/file/a5c5f17a2ec1564efdc0a.png)

![](https://telegra.ph/file/e6f9dfb662bfd75eb926d.png)

---

# It's all for now and I hope I'll continue improving project... :sunglasses: :rocket::rocket::rocket:
