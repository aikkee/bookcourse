PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE migrate_version (
	repository_id VARCHAR(250) NOT NULL, 
	repository_path TEXT, 
	version INTEGER, 
	PRIMARY KEY (repository_id)
);
INSERT INTO migrate_version VALUES('database repository','C:\Users\aikkee\workspace\htapps\htmb\db_repository',1);
CREATE TABLE resource (
        id INTEGER NOT NULL,
        rtype VARCHAR(10),
        location VARCHAR(10),
        description VARCHAR(20),
        capacity INTEGER,
        available INTEGER,
        PRIMARY KEY (id)
);
INSERT INTO resource VALUES(1,'MHA','ATT-GEN102:Re-Employment','30 DEC 2020 - 9-5pm',5,3);
INSERT INTO resource VALUES(2,'MHA','ATT-GEN102:Re-Employment','08 JAN 2021 - 9-5pm',5,5);
INSERT INTO resource VALUES(3,'MOE','ATT-GEN102:Re-Employment','14 DEC 2020 - 9-5pm',5,5);
INSERT INTO resource VALUES(4,'MOE','ATT-GEN102:Re-Employment','18 FEB 2021 - 9-5pm',5,5);
INSERT INTO resource VALUES(5,'GEN','ATT-GEN102:Re-Employment','11 DEC 2020 - 9-5pm',5,5);
INSERT INTO resource VALUES(6,'GEN','ATT-GEN102:Re-Employment','23 DEC 2020 - 9-5pm',5,5);
INSERT INTO resource VALUES(7,'GEN','ATT-GEN102:Re-Employment','04 JAN 2020 - 9-5pm',5,5);
INSERT INTO resource VALUES(8,'GEN','ATT-GEN102:Re-Employment','12 JAN 2020 - 9-5pm',5,5);
INSERT INTO resource VALUES(9,'MHA','ATT-GEN104:Part-Time Employment','04 DEC 2020 - 1-5pm',5,3);
INSERT INTO resource VALUES(10,'MOE','ATT-GEN104:Part-Time Employment','04 DEC 2020 - 1-5pm',5,5);
INSERT INTO resource VALUES(11,'MHA','ATT-GEN104:Part-Time Employment','03 MAR 2021 - 1-5pm',5,5);
INSERT INTO resource VALUES(12,'MOE','ATT-GEN104:Part-Time Employment','03 MAR 2021 - 1-5pm',5,5);
INSERT INTO resource VALUES(13,'GEN','ATT-GEN104:Part-Time Employment','26 NOV 2020 - 1-5pm',5,5);
INSERT INTO resource VALUES(14,'GEN','ATT-GEN104:Part-Time Employment','14 JAN 2021 - 1-5pm',5,5);
INSERT INTO resource VALUES(15,'GEN','ATT-GEN104:Part-Time Employment','27 JAN 2021 - 1-5pm',5,5);
INSERT INTO resource VALUES(16,'GEN','ATT-GEN104:Part-Time Employment','02 FEB 2021 - 1-5pm',5,5);
INSERT INTO resource VALUES(17,'VITAL','ATT-GEN104:Part-Time Employment','10 DEC 2020 - 1-5pm',5,5);
INSERT INTO resource VALUES(18,'VITAL','ATT-GEN104:Part-Time Employment','21 JAN 2021 - 1-5pm',5,5);
INSERT INTO resource VALUES(19,'MHA','ATT-MHA106M:Enlistment Process for HRMG','24 NOV 2020 - 9-1pm',5,5);
INSERT INTO resource VALUES(20,'MHA','ATT-MHA106M:Enlistment Process for HRMG','29 DEC 2020 - 9-1pm',5,5);
INSERT INTO resource VALUES(21,'MHA','DVP-MHA102:Training Admin-Nomination & Course','04 JAN 2021 - 9-5pm',5,5);
INSERT INTO resource VALUES(22,'MHA','DVP-MHA102:Training Admin-Nomination & Course','01 FEB 2021 - 9-5pm',5,5);
INSERT INTO resource VALUES(23,'MHA','DVP-MHA102:Training Admin-Nomination & Course','04 FEB 2021 - 9-5pm',5,5);
INSERT INTO resource VALUES(24,'MHA','DVP-MHA102:Training Admin-Nomination & Course','01 APR 2021 - 9-5pm',5,5);
INSERT INTO resource VALUES(25,'VITAL','PAY-GEN101:Pre-Payroll - Allowance & Deduction Processing and Payroll Retro Adjuster','16 NOV 2020 - 9am-1pm',5,5);
INSERT INTO resource VALUES(26,'MHA','PAY-GEN101:Pre-Payroll - Allowance & Deduction Processing and Payroll Retro Adjuster','17 NOV 2020 - 9am-1pm',5,5);
INSERT INTO resource VALUES(27,'VITAL','PAY-GEN101:Pre-Payroll - Allowance & Deduction Processing and Payroll Retro Adjuster','17 NOV 2020 - 9am-1pm',5,5);
CREATE TABLE reference (
        id INTEGER NOT NULL,
        resource_type VARCHAR(10),
        booking_ref VARCHAR(10),
        expire_on DATETIME,
        resource_id INTEGER,
        update_on DATETIME, hardcopy CHAR(1),
        PRIMARY KEY (id)
);
INSERT INTO reference VALUES(1,'MHA','mrA@mha.gov.sg**ATT-GEN102','2020-08-31 16:00:00.000000',1,'2020-08-19 12:16:12.029823',NULL);
INSERT INTO reference VALUES(2,'MHA','mrA@mha.gov.sg**ATT-GEN104','2020-08-31 16:00:00.000000',9,'2020-08-19 21:42:02.014303',NULL);
INSERT INTO reference VALUES(3,'MHA','mrA@mha.gov.sg**ATT-MHA106M','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(4,'MHA','mrA@mha.gov.sg**DVP-MHA102','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(5,'MHA','mrA@mha.gov.sg**PAY-GEN101','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(6,'MHA','mrB@mha.gov.sg**ATT-GEN102','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(7,'MHA','mrB@mha.gov.sg**ATT-GEN104','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(8,'MHA','mrB@mha.gov.sg**ATT-MHA106M','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(9,'MHA','mrB@mha.gov.sg**DVP-MHA102','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(10,'MHA','mrB@mha.gov.sg**PAY-GEN101','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(11,'MOE','mrC@moe.gov.sg**ATT-GEN102','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(12,'MOE','mrC@moe.gov.sg**ATT-GEN104','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(13,'MOE','mrD@moe.gov.sg**ATT-GEN102','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(14,'MOE','mrD@moe.gov.sg**ATT-GEN104','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(15,'VITAL','mrG@vital.gov.sg**ATT-GEN104','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(16,'VITAL','mrG@vital.gov.sg**PAY-GEN101','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(17,'VITAL','mrH@vital.gov.sg**ATT-GEN104','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(18,'VITAL','mrH@vital.gov.sg**PAY-GEN101','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(19,'GEN','mrE@psd.gov.sg**ATT-GEN102','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(20,'GEN','mrE@psd.gov.sg**ATT-GEN104','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(21,'GEN','mrF@psd.gov.sg**ATT-GEN102','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(22,'GEN','mrF@psd.gov.sg**ATT-GEN104','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(23,'GEN','mrG@vital.gov.sg**ATT-GEN102','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
INSERT INTO reference VALUES(24,'GEN','mrH@vital.gov.sg**ATT-GEN102','2020-08-31 16:00:00.000000',NULL,NULL,NULL);
COMMIT;
