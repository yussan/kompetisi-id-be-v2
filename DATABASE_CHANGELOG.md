<!-- 19 Oct 2019 -->
CREATE TABLE `kompetisiid`.`kompetisi_langganan` (
  `id_kompetisi_langganan` BIGINT(11) NOT NULL AUTO_INCREMENT,
  `id_kompetisi` BIGINT(11) NULL,
  `id_user` BIGINT(11) NULL,
  PRIMARY KEY (`id_kompetisi_langganan`),
  INDEX `kompetisi_langganan_kompetisi_idx` (`id_kompetisi` ASC) VISIBLE,
  INDEX `kompetisi_langganan_user_idx` (`id_user` ASC) VISIBLE,
  CONSTRAINT `kompetisi_langganan_kompetisi`
    FOREIGN KEY (`id_kompetisi`)
    REFERENCES `kompetisiid`.`kompetisi` (`id_kompetisi`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `kompetisi_langganan_user`
    FOREIGN KEY (`id_user`)
    REFERENCES `kompetisiid`.`user` (`id_user`)
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

