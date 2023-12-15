import database
import auth
import admin_items

def spoof_data():
    database.clear_database()

    admin1 = auth.auth_register_admin("Main", "Admin", "MainAdmin", "a@a.com", "password", database.admins, database.admin_tokens)
    admin2 = auth.auth_register_admin("Other", "Admin", "OtherAdmin", "b@b.com", "password", database.admins, database.admin_tokens)

    user1 = auth.auth_register_user("User", "One", "User1", "user1@user1.com", "password", database.users, database.user_tokens)
    user2 = auth.auth_register_user("User", "Two", "User2", "user2@user2.com", "password", database.users, database.user_tokens)

    admin_items.item_add(admin1['token'], "desk from IKEA", "", ['Furniture'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Gaming chair", "", ['Furniture', 'Gaming'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Bed", "idk its a bed", ['Furniture', 'Bedroom'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Drawer", "p", ['Furniture'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Table", "p", ['Furniture'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Controller", "For PS4", ['Gaming'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Dark Souls OST", "Composed by BlahBlah", ['Gaming', 'Music'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Fortnite Action Figure", "Made in China", ['Gaming', 'Toys'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Starcraft Ghost: Spectres", "A story about a video game", ['Gaming', 'Books'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Gaming Mouse", "Default DPI: 800", ['Gaming'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Pen", "A black pen.", ['Stationery'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Pen Holder", "It holds pens.", ['Stationery', 'Furniture'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Notebook", "You write in it", ['Stationery'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Scissors", "You cut with it", ['Stationery'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Glue", "It is sticky", ['Stationery'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Toy Gun", "Shoots harmless projectiles", ['Toys'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Hotwheels Car", "Modelled after a Ferrari", ['Toys'], 19.389, 3)
    admin_items.item_add(admin1['token'], "LEGO Set", "Star Wars LEGO Set", ['Toys'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Frisbee", "Aerodynamic", ['Toys', 'Sports'], 19.389, 3)
    admin_items.item_add(admin1['token'], "A Game of Thrones", "Dead Series", ['Books'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Beyond Good and Evil", "A book by a smart guy", ['Books'], 19.389, 3)
    admin_items.item_add(admin1['token'], "The Power of One", "A book about a South African Kid", ['Books'], 19.389, 3)
    admin_items.item_add(admin1['token'], "The Shining", "A scary book", ['Books'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Tobira: Gateway to Advanced Japanese", "This should get you N3", ['Books'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Fender Telecaster", "A classic guitar", ['Music'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Toy Guitar", "Honestly just here to have mixed tags", ['Music', 'Toys'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Unhappy Refrain", "A Vocaloid Album", ['Music'], 19.389, 3)
    admin_items.item_add(admin1['token'], "MP3 Player", "Why don't you just use your phone", ['Music'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Toilet Paper", "The currency of the New World", ['Bathroom'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Toothbrush", "To brush your teeth with", ['Bathroom'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Bathroom Mirror", "To look at yourself with", ['Bathroom', 'Furniture'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Toothbrush Holder", "Holds toiletries", ['Bathroom', 'Furniture'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Rubber Ducky", "It floats", ['Bathroom', 'Toys'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Pillow", "To lay your head on", ['Bedroom'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Night light", "Keeps monsters away", ['Bedroom'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Blanket", "Keeps you warm", ['Bedroom'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Pyjamas", "Holds toiletries", ['Bedroom'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Air Jordans", "Man he just stepped on my J's", ['Footwear', 'Sports'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Dress Shoes", "You put them on your feet", ['Footwear'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Bunny Slippers", "Cute and warm", ['Footwear', 'Bedroom'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Sneakers", "For outside wear", ['Footwear'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Basketball", "Bouncy", ['Sports'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Soccer Ball", "Soft and Bouncy", ['Sports'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Tennis Racket", "Makes a satisfying sound", ['Sports'], 19.389, 3)
    admin_items.item_add(admin1['token'], "Baseball Bat", "Hardwood bat", ['Sports'], 19.389, 3)

    admin_items.upload_item_photo(admin1['token'], 
        'https://www.ikea.com/au/en/images/products/arkelstorp-desk__0735967_PE740301_S5.JPG', 0)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/0f68fb60-84a2-4053-a92d-37aef31a7391.8c0edb46241d0602ddf74aa1f8689372.jpeg?odnHeight=612&odnWidth=612&odnBg=FFFFFF', 1)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/20421e28-3d69-4423-9aa2-11757be0d773_1.b1dbde3324bb7cce25b06bae80a1b588.jpeg?odnHeight=612&odnWidth=612&odnBg=FFFFFF', 2)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/a7129e95-6f8e-438f-920b-be8c2c1abd61_2.38ccd3670faaaa0ce444bfc5f96f341e.jpeg?odnHeight=612&odnWidth=612&odnBg=FFFFFF', 3)
    admin_items.upload_item_photo(admin1['token'], 
        'https://www.cannonhillwood.com/sites/default/files/2019-01/cIMG_1471.jpg', 4)
    admin_items.upload_item_photo(admin1['token'], 
        'https://cdn.shopify.com/s/files/1/1030/6875/products/ps4-pro-modded-controller-xmod-modchip-front_1024x1024.jpg?v=1498969253', 5)
    admin_items.upload_item_photo(admin1['token'], 
        'http://www.vgmonline.net/wp-content/uploads/49417-1424676487.jpg', 6)
    admin_items.upload_item_photo(admin1['token'], 
        'https://cdn.bmstores.co.uk/images/hpcProductImage/imgFull/346971-fortnite-core-figures-17.jpg', 7)
    admin_items.upload_item_photo(admin1['token'], 
        'https://d28hgpri8am2if.cloudfront.net/book_images/onix/cvr9781439172759/starcraft-ghost-spectres-9781439172759_hr.jpg', 8)
    admin_items.upload_item_photo(admin1['token'], 
        'https://http2.mlstatic.com/D_NQ_NP_896903-MLA44860189295_022021-V.jpg', 9)
    admin_items.upload_item_photo(admin1['token'], 
        'https://cdn.shopify.com/s/files/1/1693/8459/products/monteverde-prima-rollerball-pen-in-green-swirl_205_1024x1024.jpg?v=1571439933', 10)
    admin_items.upload_item_photo(admin1['token'], 
        'https://ae01.alicdn.com/kf/HTB1qI3tBOCYBuNkSnaVq6AMsVXaT/Durable-Office-School-Height-Pen-and-Pencil-Holder-Wired-Mesh-Design-Black-decorative-pen-holders-for.jpg', 11)
    admin_items.upload_item_photo(admin1['token'], 
        'https://ae01.alicdn.com/kf/HTB1jpvaQpXXXXcPXXXXq6xXFXXXU/Notebook-Creative-Simple-Stationery-Retro-Diary-Horizontal-Page-A5-Notebook-Student-Write-Stationery.jpg', 12)
    admin_items.upload_item_photo(admin1['token'], 
        'https://www.colichef.fr/4289/kitchen-scissors-arcos-24-cm.jpg', 13)
    admin_items.upload_item_photo(admin1['token'], 
        'https://cdnimg.webstaurantstore.com/images/products/large/382230/1683743.jpg', 14)
    admin_items.upload_item_photo(admin1['token'], 
        'http://www.pitlane-vision.com/wp-content/uploads/2018/12/nurf-gun-history-1024x682.jpg', 15)
    admin_items.upload_item_photo(admin1['token'], 
        'https://vignette.wikia.nocookie.net/hotwheels/images/1/16/Ferrari_LaFerrari_01.JPG/revision/latest/scale-to-width-down/2000?cb=20140526060247', 16)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/2cfe3839-533b-4554-92e6-a7f7bc50bcf9_1.a5d6b9f17dab12c554efce58ebe59f13.jpeg', 17)
    admin_items.upload_item_photo(admin1['token'], 
        'https://distributor.golding.eu/taurus-frisbee-blue-2-2-x-d-23-cm--10032800$1--hd.jpg', 18)
    admin_items.upload_item_photo(admin1['token'], 
        'https://georgerrmartin.com/gallery/coverart/GOThcEng.jpg', 19)
    admin_items.upload_item_photo(admin1['token'], 
        'http://i1.ebkimg.com/previews/001/001692/001692691/001692691-hq-168-80.jpg', 20)
    admin_items.upload_item_photo(admin1['token'], 
        'https://cdn2.penguin.com.au/covers/original/9780141304892.jpg', 21)
    admin_items.upload_item_photo(admin1['token'], 
        'http://thebooksmugglers.com/wp-content/uploads/2013/09/9781444720723.jpg', 22)
    admin_items.upload_item_photo(admin1['token'], 
        'https://japancentre-images.freetls.fastly.net/images/pics/10080/large/10154_tobira-gateway-textbook.jpg?1469568342', 23)
    admin_items.upload_item_photo(admin1['token'], 
        'http://www.voltageguitar.com/wp-content/uploads/2015/11/54-Fender-Telecaster-front-detail.jpg', 24)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/7aeef2f0-9ec3-4fed-bdd2-48c32a485bde_1.b07360cb6763d2bb278222ab75a0b85a.jpeg', 25)
    admin_items.upload_item_photo(admin1['token'], 
        'http://st.cdjapan.co.jp/pictures/l/08/46/DGLA-10002.jpg', 26)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/fb390ba0-b8d9-4743-905f-cf356d98da89.49486c88f7b7fa2f23d877f97926a14d.jpeg', 27)
    admin_items.upload_item_photo(admin1['token'], 
        'https://images-na.ssl-images-amazon.com/images/I/71T4EvSJamL.__AC_SY300_QL70_ML2_.jpg', 28)
    admin_items.upload_item_photo(admin1['token'], 
        'https://images-na.ssl-images-amazon.com/images/I/91PJIFsvudL.jpg', 29)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/0067ba36-49c1-42ad-80d8-369455881f62_1.beaa16d3ae90f0f69980053df21c057e.jpeg', 30)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/f4fbad10-d92e-4b38-95ec-0a97a45d06de_1.432b878f137d1dcb1f3e865dc522f360.jpeg', 31)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/de2b5600-125d-4156-a2a9-96b5e01599f6_1.766cac90414e5714ae95abc37c738838.jpeg?odnHeight=612&odnWidth=612&odnBg=FFFFFF', 32)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/192771c7-11ea-4ffa-be4b-513d13226b0a.bccbe65ec2c8a446a53267378a2a48cd.jpeg', 33)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/8dda8e47-afc7-4cca-83ed-526d482d7655_1.543cbf17b52ad689dc3e471a234122c9.jpeg?odnWidth=1000&odnHeight=1000&odnBg=ffffff', 34)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/1a00608b-ed49-4f65-ab0d-8eec733d8d08.e88f1d9cc6fd6e8e9c77597ba9097c1b.jpeg', 35)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/1e3417e9-f04c-4fc3-af4a-51426b480722.4ed8e5bdc778ccc1ebcaced7c3353f1c.jpeg', 36)
    admin_items.upload_item_photo(admin1['token'], 
        'https://thesource.com/wp-content/uploads/2019/04/air-jordan-4-bred-2019-6.jpg', 37)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/b2d54459-66b5-443a-92be-3fb178c8a2f4_1.2a012bcd964c60a1c8d016d5c531efbe.jpeg', 38)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/3301c07c-de24-455f-bc9d-866289e2ea03_1.c55ca86bafaf2935f13f139f0ad1cea3.jpeg', 39)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/d5cc4c18-352c-4103-a340-9ced7633feb1_1.4106c6bfa4365fb8adf4a7a975d28577.jpeg?odnBg=ffffff', 40)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/4336ada2-cd1d-461c-8f2e-793ce243d123_1.61088e3ca5b716e89924f3fb12aca826.jpeg', 41)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/9e24f625-cbfc-48d9-812b-92795885fd17_1.f8221810c0010582483ba1b7d9b4752e.jpeg', 42)
    admin_items.upload_item_photo(admin1['token'], 
        'https://img.tenniswarehouse-europe.com/watermark/rs.php?path=B1LS-1.jpg', 43)
    admin_items.upload_item_photo(admin1['token'], 
        'https://i5.walmartimages.com/asr/a65d995f-63b3-4427-89fe-3cbbfe6b53f9.a93dd16fbab4eaf05ffb49fe21a74788.jpeg', 44)
    admin_items.add_sales_history('12/11/2021', 1, 3)
    admin_items.add_sales_history('13/11/2021', 1, 17)
    admin_items.add_sales_history('14/11/2021', 1, 10)
    admin_items.add_sales_history('15/11/2021', 1, 13)
    admin_items.add_sales_history('16/11/2021', 1, 8)

    auth.auth_logout(admin1["token"], database.admins, database.admin_tokens)
    auth.auth_logout(admin2["token"], database.admins, database.admin_tokens)
    auth.auth_logout(user1["token"], database.users, database.user_tokens)
    auth.auth_logout(user2["token"], database.users, database.user_tokens)

    return {
        "success": True
    }

def spoof_data_lightweight():
    database.clear_database()

    admin1 = auth.auth_register_admin("Main", "Admin", "MainAdmin", "a@a.com", "password", database.admins, database.admin_tokens)
    admin2 = auth.auth_register_admin("Other", "Admin", "OtherAdmin", "b@b.com", "password", database.admins, database.admin_tokens)

    user1 = auth.auth_register_user("User", "One", "User1", "user1@user1.com", "password", database.users, database.user_tokens)
    user2 = auth.auth_register_user("User", "Two", "User2", "user2@user2.com", "password", database.users, database.user_tokens)

    admin_items.item_add(admin1['token'], "desk from IKEA", "", ['Furniture'], 19.389, 3)

    auth.auth_logout(admin1["token"], database.admins, database.admin_tokens)
    auth.auth_logout(admin2["token"], database.admins, database.admin_tokens)
    auth.auth_logout(user1["token"], database.users, database.user_tokens)
    auth.auth_logout(user2["token"], database.users, database.user_tokens)

    return {
        "success": True
    }