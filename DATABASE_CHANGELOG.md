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

