-------------------------------------------

LGE KDZ Utilities
originally
Copyright 2013 "IOMonster" (thecubed on XDA and GitHub)
Copyright 2016 Elliott Mitchell

-------------------------------------------

These two scripts will allow you to extract both KDZ files and DZ files

Run unkdz.py or undz.py with the -h option to get more options.

	-l or --list
		Lists all files contained in the archive

	-x or --extract
		Extract all portions or as chunk-files.  See -h or below for
		more detail.

	-c or --chunks
		(undz-only) Extract archive as chunks, unless a specific
		chunk number is give, all chunks will be extracted.

	-s ID or --single ID
		Extract a single slice/partition by ID (can be found with
		--list).  With undz multiple IDs can be given and the whole
		slice/partition will be extracted

	-i or --image
		(undz-only) Extract who archive as a disk image

	-d DIR or --dir DIR
		Set directory instead of the default "[kdz|dz]extracted"
		directory in the current path

	-f FILE or --file FILE
		File to operate on

A sample workflow can look like:

$ unkdz -f H90120e_00_0316.kdz -l
[+] KDZ Partition List
=========================================
 0 : H90120e_00.dz (1927680393 bytes)
 1 : LGUP_c.dll (2875560 bytes)
 2 : LGUP_c.dylib (299520000 bytes)
$ unkdz -f H90120e_00_0316.kdz -d . -s 0
[+] Extracting single partition!

[+] Extracting H90120e_00.dz to ./H90120e_00.dz
$ undz -f H90120e_00.dz -l
[!] Warning: Chunk is part of "BackupGPT", but starts in front of slice?!
[+] DZ Partition List
=========================================
 1/ 1 : PrimaryGPT_0.bin (5198 bytes)
 2/?? : _unallocated_0 (<empty>)
 3/ 2 : modem_16384.bin (42883013 bytes)
 4/?? : spare1 (<empty>)
 5/ 3 : pmic_196608.bin (11067 bytes)
 6/ 4 : sbl1_197632.bin (290344 bytes)
 7/ 5 : tz_199680.bin (258139 bytes)
 8/ 6 : sdi_201728.bin (14691 bytes)
 9/ 7 : hyp_202752.bin (23672 bytes)
10/ 8 : rpm_203776.bin (111303 bytes)
11/ 9 : aboot_204800.bin (407421 bytes)
12/10 : sbl1bak_208896.bin (290344 bytes)
13/11 : pmicbak_210944.bin (11067 bytes)
14/12 : hypbak_211968.bin (23672 bytes)
15/13 : tzbak_212992.bin (258139 bytes)
16/14 : rpmbak_215040.bin (111303 bytes)
17/15 : abootbak_216064.bin (407421 bytes)
18/16 : sdibak_220160.bin (14691 bytes)
19/?? : limits (<empty>)
20/?? : apdp (<empty>)
21/?? : msadp (<empty>)
22/?? : dpo (<empty>)
23/?? : spare2 (<empty>)
24/?? : persistent (<empty>)
25/?? : devinfo (<empty>)
26/?? : spare3 (<empty>)
27/?? : misc (<empty>)
28/17 : persist_278528.bin (23385 bytes)
29/?? : modemst1 (<empty>)
30/?? : modemst2 (<empty>)
31/?? : fsg (<empty>)
32/?? : fsc (<empty>)
33/?? : ssd (<empty>)
34/?? : keystore (<empty>)
35/?? : DDR (<empty>)
36/18 : sec_360448.bin (2603 bytes)
37/?? : encrypt (<empty>)
38/?? : eksst (<empty>)
39/19 : rct_363520.bin (2317 bytes)
40/?? : spare4 (<empty>)
41/20 : laf_376832.bin (19557377 bytes)
42/21 : boot_475136.bin (16717367 bytes)
43/22 : recovery_557056.bin (17915348 bytes)
44/?? : drm (<empty>)
45/?? : sns (<empty>)
46/?? : mpt (<empty>)
47/23 : raw_resources_737280.bin (888299 bytes)
48/24 : raw_resourcesbak_745472.bin (888299 bytes)
49/25 : factory_753664.bin (2317 bytes)
50/?? : spare5 (<empty>)
51/?? : fota (<empty>)
52/?? : fau (<empty>)
53/26 : system_901120.bin (26667953 bytes)
53/27 : system_1165448.bin (58109153 bytes)
53/28 : system_1429456.bin (54709752 bytes)
53/29 : system_1689736.bin (2313 bytes)
53/30 : system_1693784.bin (52095781 bytes)
53/31 : system_1953744.bin (70617703 bytes)
53/32 : system_2214024.bin (2313 bytes)
53/33 : system_2218072.bin (78577875 bytes)
53/34 : system_2478032.bin (48937084 bytes)
53/35 : system_2738312.bin (2313 bytes)
53/36 : system_2742360.bin (70024761 bytes)
53/37 : system_3002320.bin (66564653 bytes)
53/38 : system_3262600.bin (2313 bytes)
53/39 : system_3266648.bin (60402536 bytes)
53/40 : system_3526608.bin (62078376 bytes)
53/41 : system_3788752.bin (73287391 bytes)
53/42 : system_4050896.bin (69724602 bytes)
53/43 : system_4313040.bin (56306774 bytes)
53/44 : system_4575184.bin (55839047 bytes)
53/45 : system_4837328.bin (61357275 bytes)
53/46 : system_5099472.bin (59119265 bytes)
53/47 : system_5361616.bin (91752309 bytes)
53/48 : system_5623760.bin (62343057 bytes)
53/49 : system_5885904.bin (76765526 bytes)
53/50 : system_6148048.bin (72957287 bytes)
53/51 : system_6410192.bin (59918862 bytes)
53/52 : system_6672336.bin (61370224 bytes)
53/53 : system_6934480.bin (59869427 bytes)
53/54 : system_7196624.bin (58921312 bytes)
53/55 : system_7456904.bin (2313 bytes)
53/56 : system_7460952.bin (66004602 bytes)
53/57 : system_7720912.bin (61648352 bytes)
53/58 : system_7981192.bin (2313 bytes)
53/59 : system_7985240.bin (65414717 bytes)
53/60 : system_8245200.bin (30703423 bytes)
53/61 : system_8503296.bin (2314 bytes)
53/62 : system_8765440.bin (2314 bytes)
53/63 : system_9027584.bin (2314 bytes)
53/64 : system_9289728.bin (2314 bytes)
53/65 : system_9551872.bin (2317 bytes)
53/66 : system_9554936.bin (34407069 bytes)
54/?? : cache (<empty>)
55/?? : userdata (<empty>)
56/?? : grow (<empty>)
57/67 : BackupGPT_122141696.bin (5181 bytes)
$ undz -f H90120e_00.dz -d out -x
[!] Warning: Chunk is part of "BackupGPT", but starts in front of slice?!
[+] Extracting all chunkfiles!

[+] Extracting PrimaryGPT_0.bin to PrimaryGPT_0.bin.chunk
[+] Extracting modem_16384.bin to modem_16384.bin.chunk
[+] Extracting pmic_196608.bin to pmic_196608.bin.chunk
[+] Extracting sbl1_197632.bin to sbl1_197632.bin.chunk
[+] Extracting tz_199680.bin to tz_199680.bin.chunk
[+] Extracting sdi_201728.bin to sdi_201728.bin.chunk
[+] Extracting hyp_202752.bin to hyp_202752.bin.chunk
[+] Extracting rpm_203776.bin to rpm_203776.bin.chunk
[+] Extracting aboot_204800.bin to aboot_204800.bin.chunk
[+] Extracting sbl1bak_208896.bin to sbl1bak_208896.bin.chunk
[+] Extracting pmicbak_210944.bin to pmicbak_210944.bin.chunk
[+] Extracting hypbak_211968.bin to hypbak_211968.bin.chunk
[+] Extracting tzbak_212992.bin to tzbak_212992.bin.chunk
[+] Extracting rpmbak_215040.bin to rpmbak_215040.bin.chunk
[+] Extracting abootbak_216064.bin to abootbak_216064.bin.chunk
[+] Extracting sdibak_220160.bin to sdibak_220160.bin.chunk
[+] Extracting persist_278528.bin to persist_278528.bin.chunk
[+] Extracting sec_360448.bin to sec_360448.bin.chunk
[+] Extracting rct_363520.bin to rct_363520.bin.chunk
[+] Extracting laf_376832.bin to laf_376832.bin.chunk
[+] Extracting boot_475136.bin to boot_475136.bin.chunk
[+] Extracting recovery_557056.bin to recovery_557056.bin.chunk
[+] Extracting raw_resources_737280.bin to raw_resources_737280.bin.chunk
[+] Extracting raw_resourcesbak_745472.bin to raw_resourcesbak_745472.bin.chunk
[+] Extracting factory_753664.bin to factory_753664.bin.chunk
[+] Extracting system_901120.bin to system_901120.bin.chunk
[+] Extracting system_1165448.bin to system_1165448.bin.chunk
[+] Extracting system_1429456.bin to system_1429456.bin.chunk
[+] Extracting system_1689736.bin to system_1689736.bin.chunk
[+] Extracting system_1693784.bin to system_1693784.bin.chunk
[+] Extracting system_1953744.bin to system_1953744.bin.chunk
[+] Extracting system_2214024.bin to system_2214024.bin.chunk
[+] Extracting system_2218072.bin to system_2218072.bin.chunk
[+] Extracting system_2478032.bin to system_2478032.bin.chunk
[+] Extracting system_2738312.bin to system_2738312.bin.chunk
[+] Extracting system_2742360.bin to system_2742360.bin.chunk
[+] Extracting system_3002320.bin to system_3002320.bin.chunk
[+] Extracting system_3262600.bin to system_3262600.bin.chunk
[+] Extracting system_3266648.bin to system_3266648.bin.chunk
[+] Extracting system_3526608.bin to system_3526608.bin.chunk
[+] Extracting system_3788752.bin to system_3788752.bin.chunk
[+] Extracting system_4050896.bin to system_4050896.bin.chunk
[+] Extracting system_4313040.bin to system_4313040.bin.chunk
[+] Extracting system_4575184.bin to system_4575184.bin.chunk
[+] Extracting system_4837328.bin to system_4837328.bin.chunk
[+] Extracting system_5099472.bin to system_5099472.bin.chunk
[+] Extracting system_5361616.bin to system_5361616.bin.chunk
[+] Extracting system_5623760.bin to system_5623760.bin.chunk
[+] Extracting system_5885904.bin to system_5885904.bin.chunk
[+] Extracting system_6148048.bin to system_6148048.bin.chunk
[+] Extracting system_6410192.bin to system_6410192.bin.chunk
[+] Extracting system_6672336.bin to system_6672336.bin.chunk
[+] Extracting system_6934480.bin to system_6934480.bin.chunk
[+] Extracting system_7196624.bin to system_7196624.bin.chunk
[+] Extracting system_7456904.bin to system_7456904.bin.chunk
[+] Extracting system_7460952.bin to system_7460952.bin.chunk
[+] Extracting system_7720912.bin to system_7720912.bin.chunk
[+] Extracting system_7981192.bin to system_7981192.bin.chunk
[+] Extracting system_7985240.bin to system_7985240.bin.chunk
[+] Extracting system_8245200.bin to system_8245200.bin.chunk
[+] Extracting system_8503296.bin to system_8503296.bin.chunk
[+] Extracting system_8765440.bin to system_8765440.bin.chunk
[+] Extracting system_9027584.bin to system_9027584.bin.chunk
[+] Extracting system_9289728.bin to system_9289728.bin.chunk
[+] Extracting system_9551872.bin to system_9551872.bin.chunk
[+] Extracting system_9554936.bin to system_9554936.bin.chunk
[+] Extracting BackupGPT_122141696.bin to BackupGPT_122141696.bin.chunk
$ del out/system_*
$ undz -f H90120e_00.dz -d out -s 53
[!] Warning: Chunk is part of "BackupGPT", but starts in front of slice?!
[+] Extracting single slice^Wpartition!

[+] Extracting system_901120.bin to system.image
[+] Extracting system_1165448.bin to system.image
[+] Extracting system_1429456.bin to system.image
[+] Extracting system_1689736.bin to system.image
[+] Extracting system_1693784.bin to system.image
[+] Extracting system_1953744.bin to system.image
[+] Extracting system_2214024.bin to system.image
[+] Extracting system_2218072.bin to system.image
[+] Extracting system_2478032.bin to system.image
[+] Extracting system_2738312.bin to system.image
[+] Extracting system_2742360.bin to system.image
[+] Extracting system_3002320.bin to system.image
[+] Extracting system_3262600.bin to system.image
[+] Extracting system_3266648.bin to system.image
[+] Extracting system_3526608.bin to system.image
[+] Extracting system_3788752.bin to system.image
[+] Extracting system_4050896.bin to system.image
[+] Extracting system_4313040.bin to system.image
[+] Extracting system_4575184.bin to system.image
[+] Extracting system_4837328.bin to system.image
[+] Extracting system_5099472.bin to system.image
[+] Extracting system_5361616.bin to system.image
[+] Extracting system_5623760.bin to system.image
[+] Extracting system_5885904.bin to system.image
[+] Extracting system_6148048.bin to system.image
[+] Extracting system_6410192.bin to system.image
[+] Extracting system_6672336.bin to system.image
[+] Extracting system_6934480.bin to system.image
[+] Extracting system_7196624.bin to system.image
[+] Extracting system_7456904.bin to system.image
[+] Extracting system_7460952.bin to system.image
[+] Extracting system_7720912.bin to system.image
[+] Extracting system_7981192.bin to system.image
[+] Extracting system_7985240.bin to system.image
[+] Extracting system_8245200.bin to system.image
[+] Extracting system_8503296.bin to system.image
[+] Extracting system_8765440.bin to system.image
[+] Extracting system_9027584.bin to system.image
[+] Extracting system_9289728.bin to system.image
[+] Extracting system_9551872.bin to system.image
[+] Extracting system_9554936.bin to system.image
$ 

At this point you can modify out/system.image to your liking.  For this
particular device (LG H901), system.image is an EXT4 filesystem.  Many tools
exist for modifying EXT4 filesystems and these should work fine.

The next step would be reconstructing the file.  There are two steps, turning
the files into chunks and then merging them together into a DZ file.  As of
this writing, "image2chunks.py" relies on the Operating System and filesystem
having support for SEEK_DATA/SEEK_HOLE.  Holes are used on Unix to indicate
portions of files which do not have any data blocks allocated to them.  It may
be possible to simulate this on Windows, but this has not yet been implemented.

If system.image is placed on a filesystem which lacks support for
SEEK_DATA/SEEK_HOLE, the whole diskslice/partition will end up being
represented by a single huge chunk.  This should in fact work, but is rather
suboptimal.  I suspect keeping system.image on an EXT4 filesystem will be
ideal, since I suspect the technique I'm using is similar to what LG is using
and I suspect they're using EXT4.

$ image2chunks out/system.image
[+] Compressing system.image to system_901120.bin (1160 empty blocks)
[+] Compressing system.image to system_1165448.bin (3912 empty blocks)
[+] Compressing system.image to system_1429456.bin (1208 empty blocks)
[+] Compressing system.image to system_1689736.bin (3024 empty blocks)
[+] Compressing system.image to system_1693784.bin (3960 empty blocks)
[+] Compressing system.image to system_1953744.bin (1208 empty blocks)
[+] Compressing system.image to system_2214024.bin (3024 empty blocks)
[+] Compressing system.image to system_2218072.bin (3960 empty blocks)
[+] Compressing system.image to system_2478032.bin (1208 empty blocks)
[+] Compressing system.image to system_2738312.bin (3024 empty blocks)
[+] Compressing system.image to system_2742360.bin (3960 empty blocks)
[+] Compressing system.image to system_3002320.bin (1208 empty blocks)
[+] Compressing system.image to system_3262600.bin (3024 empty blocks)
[+] Compressing system.image to system_3266648.bin (3960 empty blocks)
[+] Compressing system.image to system_3526608.bin (3072 empty blocks)
[+] Compressing system.image to system_3788752.bin (3072 empty blocks)
[+] Compressing system.image to system_4050896.bin (3072 empty blocks)
[+] Compressing system.image to system_4313040.bin (3072 empty blocks)
[+] Compressing system.image to system_4575184.bin (3072 empty blocks)
[+] Compressing system.image to system_4837328.bin (3072 empty blocks)
[+] Compressing system.image to system_5099472.bin (3072 empty blocks)
[+] Compressing system.image to system_5361616.bin (3072 empty blocks)
[+] Compressing system.image to system_5623760.bin (3072 empty blocks)
[+] Compressing system.image to system_5885904.bin (3072 empty blocks)
[+] Compressing system.image to system_6148048.bin (3072 empty blocks)
[+] Compressing system.image to system_6410192.bin (3072 empty blocks)
[+] Compressing system.image to system_6672336.bin (3072 empty blocks)
[+] Compressing system.image to system_6934480.bin (3072 empty blocks)
[+] Compressing system.image to system_7196624.bin (1208 empty blocks)
[+] Compressing system.image to system_7456904.bin (3024 empty blocks)
[+] Compressing system.image to system_7460952.bin (3960 empty blocks)
[+] Compressing system.image to system_7720912.bin (1208 empty blocks)
[+] Compressing system.image to system_7981192.bin (3024 empty blocks)
[+] Compressing system.image to system_7985240.bin (3960 empty blocks)
[+] Compressing system.image to system_8245200.bin (132144 empty blocks)
[+] Compressing system.image to system_8503296.bin (261120 empty blocks)
[+] Compressing system.image to system_8765440.bin (261120 empty blocks)
[+] Compressing system.image to system_9027584.bin (261120 empty blocks)
[+] Compressing system.image to system_9289728.bin (261120 empty blocks)
[+] Compressing system.image to system_9551872.bin (2040 empty blocks)
[+] Compressing system.image to system_9554936.bin (8 empty blocks)
[+] done
$ mkdz -f test.dz -d out -m
[+] Writing 67 chunks to test.dz:

[+] Writing PrimaryGPT_0.bin.chunk to test.dz (5710 bytes)
[+] Writing modem_16384.bin.chunk to test.dz (42883525 bytes)
[+] Writing pmic_196608.bin.chunk to test.dz (11579 bytes)
[+] Writing sbl1_197632.bin.chunk to test.dz (290856 bytes)
[+] Writing tz_199680.bin.chunk to test.dz (258651 bytes)
[+] Writing sdi_201728.bin.chunk to test.dz (15203 bytes)
[+] Writing hyp_202752.bin.chunk to test.dz (24184 bytes)
[+] Writing rpm_203776.bin.chunk to test.dz (111815 bytes)
[+] Writing aboot_204800.bin.chunk to test.dz (407933 bytes)
[+] Writing sbl1bak_208896.bin.chunk to test.dz (290856 bytes)
[+] Writing pmicbak_210944.bin.chunk to test.dz (11579 bytes)
[+] Writing hypbak_211968.bin.chunk to test.dz (24184 bytes)
[+] Writing tzbak_212992.bin.chunk to test.dz (258651 bytes)
[+] Writing rpmbak_215040.bin.chunk to test.dz (111815 bytes)
[+] Writing abootbak_216064.bin.chunk to test.dz (407933 bytes)
[+] Writing sdibak_220160.bin.chunk to test.dz (15203 bytes)
[+] Writing persist_278528.bin.chunk to test.dz (23897 bytes)
[+] Writing sec_360448.bin.chunk to test.dz (3115 bytes)
[+] Writing rct_363520.bin.chunk to test.dz (2829 bytes)
[+] Writing laf_376832.bin.chunk to test.dz (19557889 bytes)
[+] Writing boot_475136.bin.chunk to test.dz (16717879 bytes)
[+] Writing recovery_557056.bin.chunk to test.dz (17915860 bytes)
[+] Writing raw_resources_737280.bin.chunk to test.dz (888811 bytes)
[+] Writing raw_resourcesbak_745472.bin.chunk to test.dz (888811 bytes)
[+] Writing factory_753664.bin.chunk to test.dz (2829 bytes)
[+] Writing system_901120.bin.chunk to test.dz (26668465 bytes)
[+] Writing system_1165448.bin.chunk to test.dz (58109665 bytes)
[+] Writing system_1429456.bin.chunk to test.dz (54710264 bytes)
[+] Writing system_1689736.bin.chunk to test.dz (2825 bytes)
[+] Writing system_1693784.bin.chunk to test.dz (52096293 bytes)
[+] Writing system_1953744.bin.chunk to test.dz (70618215 bytes)
[+] Writing system_2214024.bin.chunk to test.dz (2825 bytes)
[+] Writing system_2218072.bin.chunk to test.dz (78578387 bytes)
[+] Writing system_2478032.bin.chunk to test.dz (48937596 bytes)
[+] Writing system_2738312.bin.chunk to test.dz (2825 bytes)
[+] Writing system_2742360.bin.chunk to test.dz (70025273 bytes)
[+] Writing system_3002320.bin.chunk to test.dz (66565165 bytes)
[+] Writing system_3262600.bin.chunk to test.dz (2825 bytes)
[+] Writing system_3266648.bin.chunk to test.dz (60403048 bytes)
[+] Writing system_3526608.bin.chunk to test.dz (62078888 bytes)
[+] Writing system_3788752.bin.chunk to test.dz (73287903 bytes)
[+] Writing system_4050896.bin.chunk to test.dz (69725114 bytes)
[+] Writing system_4313040.bin.chunk to test.dz (56307286 bytes)
[+] Writing system_4575184.bin.chunk to test.dz (55839559 bytes)
[+] Writing system_4837328.bin.chunk to test.dz (61357787 bytes)
[+] Writing system_5099472.bin.chunk to test.dz (59119777 bytes)
[+] Writing system_5361616.bin.chunk to test.dz (91752821 bytes)
[+] Writing system_5623760.bin.chunk to test.dz (62343569 bytes)
[+] Writing system_5885904.bin.chunk to test.dz (76766038 bytes)
[+] Writing system_6148048.bin.chunk to test.dz (72957799 bytes)
[+] Writing system_6410192.bin.chunk to test.dz (59919374 bytes)
[+] Writing system_6672336.bin.chunk to test.dz (61370736 bytes)
[+] Writing system_6934480.bin.chunk to test.dz (59869939 bytes)
[+] Writing system_7196624.bin.chunk to test.dz (58921824 bytes)
[+] Writing system_7456904.bin.chunk to test.dz (2825 bytes)
[+] Writing system_7460952.bin.chunk to test.dz (66005114 bytes)
[+] Writing system_7720912.bin.chunk to test.dz (61648864 bytes)
[+] Writing system_7981192.bin.chunk to test.dz (2825 bytes)
[+] Writing system_7985240.bin.chunk to test.dz (65415229 bytes)
[+] Writing system_8245200.bin.chunk to test.dz (30703935 bytes)
[+] Writing system_8503296.bin.chunk to test.dz (2826 bytes)
[+] Writing system_8765440.bin.chunk to test.dz (2826 bytes)
[+] Writing system_9027584.bin.chunk to test.dz (2826 bytes)
[+] Writing system_9289728.bin.chunk to test.dz (2826 bytes)
[+] Writing system_9551872.bin.chunk to test.dz (2829 bytes)
[+] Writing system_9554936.bin.chunk to test.dz (34407581 bytes)
[+] Writing BackupGPT_122141696.bin.chunk to test.dz (5693 bytes)
$ 

At this point if test.dz is compared to the original H90120e_00_0316.kdz, they
should be identical.  As stated above, this has only been shown to produce an
identical file when operating on Linux and using EXT4.  EXT2/3 may also work if
mounted using the EXT4's backwards compatibility mode, rather than the native
implementation of EXT2/3.  Most other flavors of Unix should get sane output,
but not as likely to be identical, differing size of filesystem holes may have
an important effect.

There is a value in the chunk headers referred to as "wipeCount" in the code,
as well as in the .params files (these are simply text files) generated for
extracted slices.  My suspicion is this is this is a count of blocks to be
TRIMed prior to writing the data from the DZ file.  There are some oddities
though, notably several slices/partitions are marked as being wiped by a
large value on the prior chunk.  I'm unsure what this means, perhaps LG's tools
ignore super large wipes.

There is also the quirk of the backup GPT's chunk extending near the front of
the "grow" slice/partition.  My suspicion is this is a weakness of the tools LG
is using to generate the files.  Perhaps they don't understand the concept of
chunks which don't start at a slice/partition boundary, they also may not
correctly handle the case of chunks which *begin* with a hole.

Lastly, I'm concerned about the number of unknowns in the DZ header.  Several
look to be harmless to simply copy the value from an existing file, but others
are totally unknown to me at this time.  Two fields look to be date codes of
some flavor (easy, simply copy).  I worry more of these need to be regenerated,
but I've got no idea what to put in new files.


-------------------------------------------

Permission was granted to rerelease this software as long as attribution was
given.  This version is distributed under the terms of the GNU Public License
version 3.

-------------------------------------------

