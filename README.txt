-------------------------------------------

LGE KDZ Utilities
originally by IOMonster (thecubed on XDA)

-------------------------------------------

These two scripts will allow you to extract both KDZ files and DZ files

Run kdzfiletools.py or dzfiletools.py with the -h option to get more options.

	-l or --list
		Lists all files contained in the archive

	-x or --extract
		Extract all files in the archive

	-s ID or --single ID
		Extract a single partition by ID (can be found with --list)

	-o DIR or --out DIR
		Set output directory instead of the default "[kdz|dz]extracted" directory
		in the current path

	-f FILE or --file FILE
		Input file to operate on

A simple method to extract a KDZ file is as follows:

# python KDZFileTools.py -f LAS_V08d_pre3_00.kdz -x
[+] KDZ Partition List
=========================================
 0 : LAS_V08d_pre3_00.dz (1428092632 bytes)
 1 : LGUP_8974.dll (1477632 bytes)

# python KDZFileTools.py -f LAS_V08d_pre3_00.kdz -s 0 
[+] Extracting single partition!

[+] Extracting LAS_V08d_pre3_00.dz to kdzextracted/LAS_V08d_pre3_00.dz

# python DZFileTools.py -f kdzextracted/LAS_V08d_pre3_00.dz -l
[+] DZ Partition List
=========================================
 0 : PrimaryGPT_0.bin (4299 bytes)
 1 : modem_32768.bin (25719664 bytes)
 2 : sbl1_163840.bin (179443 bytes)
 3 : dbi_165888.bin (10505 bytes)
 4 : aboot_229376.bin (288082 bytes)
 5 : rpm_231424.bin (93084 bytes)
 6 : boot_262144.bin (8959565 bytes)
 7 : tz_294912.bin (149388 bytes)
 8 : persist_393216.bin (23621 bytes)
 9 : recovery_458752.bin (10454494 bytes)
10 : laf_622592.bin (14244284 bytes)
11 : system_7176192.bin (66791740 bytes)
12 : system_7438336.bin (2651 bytes)
13 : system_7440008.bin (2313 bytes)
14 : system_7444120.bin (103727934 bytes)
15 : system_7704592.bin (114239263 bytes)
16 : system_7964296.bin (2313 bytes)
17 : system_7968408.bin (103349001 bytes)
18 : system_8228880.bin (121921125 bytes)
19 : system_8488584.bin (2313 bytes)
20 : system_8492696.bin (101078725 bytes)
21 : system_8753168.bin (125454806 bytes)
22 : system_9012872.bin (2313 bytes)
23 : system_9016984.bin (105806605 bytes)
24 : system_9277456.bin (115830981 bytes)
25 : system_9537160.bin (2313 bytes)
26 : system_9541272.bin (108458465 bytes)
27 : system_9801744.bin (83280847 bytes)
28 : system_10063888.bin (67940827 bytes)
29 : system_10326032.bin (91997923 bytes)
30 : system_10588176.bin (58015487 bytes)
31 : system_10846208.bin (2314 bytes)
32 : system_11108352.bin (2314 bytes)
33 : system_11370496.bin (2314 bytes)
34 : system_11632640.bin (2314 bytes)
35 : system_11894784.bin (2314 bytes)
36 : system_12156928.bin (2314 bytes)
37 : system_12419072.bin (2314 bytes)
38 : system_12681216.bin (2314 bytes)
39 : system_12943360.bin (2314 bytes)
40 : system_13205504.bin (2314 bytes)
41 : system_13467648.bin (2314 bytes)
42 : system_13729792.bin (2652 bytes)
43 : system_13731464.bin (2314 bytes)
44 : BackupGPT_61070336.bin (4286 bytes)

From here, you can simply run the following command to extract a specific partition, or use -x to extract all:

# python DZFileTools.py -f kdzextracted/LAS_V08d_pre3_00.dz -s 4



-------------------------------------------

Permission was granted to rerelease this software as long as attribution was
given.  This version is distributed under the terms of the GNU Public License
version 3.

-------------------------------------------
