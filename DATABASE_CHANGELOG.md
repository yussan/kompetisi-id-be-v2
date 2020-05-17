<!-- 17 May 2020 -->
<!-- remove same tags first before execute it -->

ALTER TABLE `tags`
CHANGE COLUMN `tag` `tag` VARCHAR(150) NOT NULL ,
ADD UNIQUE INDEX `tag_UNIQUE` (`tag` ASC);
;

ALTER TABLE `sub_kat`
ADD UNIQUE INDEX `sub_kat_UNIQUE` (`sub_kat` ASC);
;

ALTER TABLE `main_kat`
ADD UNIQUE INDEX `main_kat_UNIQUE` (`main_kat` ASC),
ADD UNIQUE INDEX `logo_UNIQUE` (`logo` ASC),
ADD UNIQUE INDEX `color_UNIQUE` (`color` ASC),
ADD UNIQUE INDEX `deskripsi_UNIQUE` (`deskripsi` ASC);
;

ALTER TABLE `user`
CHANGE COLUMN `username` `username` VARCHAR(50) NOT NULL ,
CHANGE COLUMN `user_key` `user_key` TEXT NULL ,
ADD UNIQUE INDEX `email_UNIQUE` (`email` ASC);
;

DROP TABLE `kompetisi_diskusi`;

ALTER TABLE `email_token`
CHANGE COLUMN `token` `token` VARCHAR(200) NOT NULL ,
ADD UNIQUE INDEX `token_UNIQUE` (`token` ASC);
;

ALTER TABLE `kompetisi_btn`
ADD INDEX `kompetisi_user_INDEX` (`id_kompetisi` ASC, `id_user` ASC);
;

ALTER TABLE `kompetisi_langganan`
DROP FOREIGN KEY `kompetisi_langganan_kompetisi`,
DROP FOREIGN KEY `kompetisi_langganan_user`;
ALTER TABLE `kompetisi_langganan`
CHANGE COLUMN `id_kompetisi` `id_kompetisi` BIGINT(11) NOT NULL ,
CHANGE COLUMN `id_user` `id_user` BIGINT(11) NOT NULL ,
ADD INDEX `kompetisi_user_INDEX` (`id_kompetisi` ASC, `id_user` ASC);
;
ALTER TABLE `kompetisi_langganan`
ADD CONSTRAINT `kompetisi_langganan_kompetisi`
FOREIGN KEY (`id_kompetisi`)
REFERENCES `kompetisi` (`id_kompetisi`)
ON DELETE NO ACTION
ON UPDATE NO ACTION,
ADD CONSTRAINT `kompetisi_langganan_user`
FOREIGN KEY (`id_user`)
REFERENCES `user` (`id_user`)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

<!-- 20 Oct 2020 -->

CREATE TABLE `kompetisi_langganan` (
`id_kompetisi_langganan` bigint(11) NOT NULL AUTO_INCREMENT,
`id_kompetisi` bigint(11) DEFAULT NULL,
`id_user` bigint(11) DEFAULT NULL,
PRIMARY KEY (`id_kompetisi_langganan`),
KEY `kompetisi_langganan_kompetisi_idx` (`id_kompetisi`),
KEY `kompetisi_langganan_user_idx` (`id_user`),
CONSTRAINT `kompetisi_langganan_kompetisi` FOREIGN KEY (`id_kompetisi`) REFERENCES `kompetisi` (`id_kompetisi`) ON DELETE NO ACTION ON UPDATE NO ACTION,
CONSTRAINT `kompetisi_langganan_user` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

<!-- 19 Oct 2019 -->

CREATE TABLE `kompetisi_langganan` (
`id_kompetisi_langganan` BIGINT(11) NOT NULL AUTO_INCREMENT,
`id_kompetisi` BIGINT(11) NULL,
`id_user` BIGINT(11) NULL,
PRIMARY KEY (`id_kompetisi_langganan`),
INDEX `kompetisi_langganan_kompetisi_idx` (`id_user` ASC),
CONSTRAINT `kompetisi_langganan_kompetisi`
FOREIGN KEY (`id_user`)
REFERENCES `ki-4.1`.`kompetisi` (`id_kompetisi`)
ON DELETE NO ACTION
ON UPDATE NO ACTION,
CONSTRAINT `kompetisi_langganan_user`
FOREIGN KEY (`id_user`)
REFERENCES `ki-4.1`.`user` (`id_user`)
ON DELETE NO ACTION
ON UPDATE NO ACTION);

<!-- 27 jun 2019 -->

ALTER TABLE `kompetisiid`.`berita`
ADD COLUMN `draft` ENUM('0', '1') NULL DEFAULT '0' AFTER `tag`;

ALTER TABLE `ki-4.1`.`kompetisi`
CHANGE COLUMN `draft` ENUM('0', '1') NULL DEFAULT '0' ;

<!-- 9 jun 2019 -->

ALTER TABLE `user_token`
ADD COLUMN `token_type` ENUM("forgot-email") NULL AFTER `expired`;

<!-- 31 Mei 2019
alter tabel kompetisi_btn.tandai to kompetisi_btn.like -->

ALTER TABLE `kompetisi_btn`
CHANGE COLUMN `tandai` `like` INT(11) NULL DEFAULT NULL ;

<!-- 31 Mei 2019
add primary key on table kompetisi.btn -->

ALTER TABLE `kompetisi_btn`
ADD COLUMN `id` BIGINT(11) NOT NULL AUTO_INCREMENT AFTER `verified`,
ADD PRIMARY KEY (`id`);
ALTER TABLE `kompetisi_btn`
CHANGE COLUMN `id` `id` BIGINT(11) NOT NULL AUTO_INCREMENT FIRST;
