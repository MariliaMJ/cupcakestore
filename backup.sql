BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "accounts_account" (
	"id"	integer NOT NULL,
	"password"	varchar(128) NOT NULL,
	"first_name"	varchar(50) NOT NULL,
	"last_name"	varchar(50) NOT NULL,
	"username"	varchar(50) NOT NULL UNIQUE,
	"email"	varchar(100) NOT NULL UNIQUE,
	"phone_number"	varchar(50) NOT NULL,
	"date_joined"	datetime NOT NULL,
	"last_login"	datetime NOT NULL,
	"is_admin"	bool NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"is_superadmin"	bool NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "store_product" (
	"id"	char(32) NOT NULL,
	"name"	varchar(100) NOT NULL,
	"flavor"	varchar(100) NOT NULL,
	"icing"	text NOT NULL,
	"filling"	text NOT NULL,
	"price"	decimal NOT NULL,
	"image"	varchar(200) NOT NULL,
	"inventory"	integer NOT NULL,
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"is_available"	bool NOT NULL,
	PRIMARY KEY("id")
);
INSERT INTO "accounts_account" VALUES (1,'pbkdf2_sha256$600000$mp3hljeVROTIQjotycJiV8$NeV+yVXqQOhUOHzXbZ6I9hjHfRqAwrde59y731T26sw=','admin','admin','admin','admin@admin.com','','2023-11-24 04:33:00.964066','2023-11-24 04:34:58.254607',1,1,1,1);
INSERT INTO "auth_permission" VALUES (1,1,'add_logentry','Can add log entry'),
 (2,1,'change_logentry','Can change log entry'),
 (3,1,'delete_logentry','Can delete log entry'),
 (4,1,'view_logentry','Can view log entry'),
 (5,2,'add_permission','Can add permission'),
 (6,2,'change_permission','Can change permission'),
 (7,2,'delete_permission','Can delete permission'),
 (8,2,'view_permission','Can view permission'),
 (9,3,'add_group','Can add group'),
 (10,3,'change_group','Can change group'),
 (11,3,'delete_group','Can delete group'),
 (12,3,'view_group','Can view group'),
 (13,4,'add_contenttype','Can add content type'),
 (14,4,'change_contenttype','Can change content type'),
 (15,4,'delete_contenttype','Can delete content type'),
 (16,4,'view_contenttype','Can view content type'),
 (17,5,'add_session','Can add session'),
 (18,5,'change_session','Can change session'),
 (19,5,'delete_session','Can delete session'),
 (20,5,'view_session','Can view session'),
 (21,6,'add_address','Can add address'),
 (22,6,'change_address','Can change address'),
 (23,6,'delete_address','Can delete address'),
 (24,6,'view_address','Can view address'),
 (25,7,'add_cupcake','Can add cupcake'),
 (26,7,'change_cupcake','Can change cupcake'),
 (27,7,'delete_cupcake','Can delete cupcake'),
 (28,7,'view_cupcake','Can view cupcake'),
 (29,8,'add_customer','Can add customer'),
 (30,8,'change_customer','Can change customer'),
 (31,8,'delete_customer','Can delete customer'),
 (32,8,'view_customer','Can view customer'),
 (33,9,'add_account','Can add account'),
 (34,9,'change_account','Can change account'),
 (35,9,'delete_account','Can delete account'),
 (36,9,'view_account','Can view account'),
 (37,10,'add_product','Can add product'),
 (38,10,'change_product','Can change product'),
 (39,10,'delete_product','Can delete product'),
 (40,10,'view_product','Can view product'),
 (41,11,'add_cart','Can add cart'),
 (42,11,'change_cart','Can change cart'),
 (43,11,'delete_cart','Can delete cart'),
 (44,11,'view_cart','Can view cart'),
 (45,12,'add_cartitem','Can add cart item'),
 (46,12,'change_cartitem','Can change cart item'),
 (47,12,'delete_cartitem','Can delete cart item'),
 (48,12,'view_cartitem','Can view cart item'),
 (49,13,'add_order','Can add order'),
 (50,13,'change_order','Can change order'),
 (51,13,'delete_order','Can delete order'),
 (52,13,'view_order','Can view order'),
 (53,14,'add_itemorder','Can add item order'),
 (54,14,'change_itemorder','Can change item order'),
 (55,14,'delete_itemorder','Can delete item order'),
 (56,14,'view_itemorder','Can view item order');
INSERT INTO "store_product" VALUES ('472b700aeeb34fd381c5f234cab11d02','Cupcake de chocolate','chocolate','Brigadeiro','Brigadeiro',10,'https://www.receitasnestle.com.br/sites/default/files/srh_recipes/0fff5f03afb90bb990364a480f294cd7.jpg',10,'2023-11-24 04:36:00.599499','2023-11-24 04:36:00.599529',1),
 ('7a469f294b0d49d49c250ad3118bb651','Cupcake de baunilha','massa branca','Buttercream','Buttercream',10,'https://www.receitasnestle.com.br/sites/default/files/srh_recipes/0fff5f03afb90bb990364a480f294cd7.jpg',10,'2023-11-24 04:37:09.096726','2023-11-24 04:37:09.096772',1),
 ('889a24c231cb429a8bd7f9b6ccfe36f4','Cupcake de morango','massa branca','Buttercream','Geleia',15,'https://www.receitasnestle.com.br/sites/default/files/srh_recipes/0fff5f03afb90bb990364a480f294cd7.jpg',5,'2023-11-24 04:37:41.311322','2023-11-24 04:37:41.311365',1),
 ('6909172fdce54ecb93d242435c3a008f','Cupcake de ovomaltine','chocolate','Buttercream de chocolate','Brigadeiro de chocolate',20,'https://www.receitasnestle.com.br/sites/default/files/srh_recipes/0fff5f03afb90bb990364a480f294cd7.jpg',5,'2023-11-24 04:38:13.824994','2023-11-24 04:38:13.825045',1),
 ('4cafd42064404384b8c7f4be57b011fa','Cupcake de limão','massa branca','buttercream de limão','brigadeiro de limão',10,'https://www.receitasnestle.com.br/sites/default/files/srh_recipes/0fff5f03afb90bb990364a480f294cd7.jpg',5,'2023-11-24 04:40:26.993306','2023-11-24 04:40:26.993352',1);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
COMMIT;
