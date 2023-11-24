BEGIN TRANSACTION;
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
INSERT INTO "store_product" VALUES ('472b700aeeb34fd381c5f234cab11d02','Cupcake de chocolate','chocolate','Brigadeiro','Brigadeiro',10,'https://www.receitasnestle.com.br/sites/default/files/srh_recipes/0fff5f03afb90bb990364a480f294cd7.jpg',10,'2023-11-24 04:36:00.599499','2023-11-24 04:36:00.599529',1),
 ('7a469f294b0d49d49c250ad3118bb651','Cupcake de baunilha','massa branca','Buttercream','Buttercream',10,'https://www.receitasnestle.com.br/sites/default/files/srh_recipes/0fff5f03afb90bb990364a480f294cd7.jpg',10,'2023-11-24 04:37:09.096726','2023-11-24 04:37:09.096772',1),
 ('889a24c231cb429a8bd7f9b6ccfe36f4','Cupcake de morango','massa branca','Buttercream','Geleia',15,'https://www.receitasnestle.com.br/sites/default/files/srh_recipes/0fff5f03afb90bb990364a480f294cd7.jpg',5,'2023-11-24 04:37:41.311322','2023-11-24 04:37:41.311365',1),
 ('6909172fdce54ecb93d242435c3a008f','Cupcake de ovomaltine','chocolate','Buttercream de chocolate','Brigadeiro de chocolate',20,'https://www.receitasnestle.com.br/sites/default/files/srh_recipes/0fff5f03afb90bb990364a480f294cd7.jpg',5,'2023-11-24 04:38:13.824994','2023-11-24 04:38:13.825045',1),
 ('4cafd42064404384b8c7f4be57b011fa','Cupcake de limão','massa branca','buttercream de limão','brigadeiro de limão',10,'https://www.receitasnestle.com.br/sites/default/files/srh_recipes/0fff5f03afb90bb990364a480f294cd7.jpg',5,'2023-11-24 04:40:26.993306','2023-11-24 04:40:26.993352',1);
COMMIT;
