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

$ unkdz -f H90120j_00_0712.kdz -l
[+] KDZ Partition List (format v2)
=========================================
 0 : H90120j_00.dz (1988019978 bytes)
 1 : LGUP_c.dll (2875560 bytes)
 2 : LGUP_c.dylib (1170000 bytes)
$ unkdz -f H90120j_00_0712.kdz -x
[+] Extracting all partitions from v2 file!

[+] Extracting H90120e_00.dz to kdzextracted/H90120j_00.dz
[+] Extracting LGUP_c.dll to kdzextracted/LGUP_c.dll
[+] Extracting LGUP_c.dylib to kdzextracted/LGUP_c.dylib
$ undz -f kdzextracted/H90120j_00.dz -l
[!] Warning: Chunk is part of "BackupGPT", but starts in front of slice?!
[+] DZ Partition List
=========================================
 0/ 1 : PrimaryGPT_0.bin (5199 bytes)
-1/?? : _unallocated_0_8371200 (<empty>)
 1/ 2 : modem_16384.bin (42902300 bytes)
 2/?? : spare1 (<empty>)
 3/ 3 : pmic_196608.bin (11065 bytes)
 4/ 4 : sbl1_197632.bin (290373 bytes)
 5/ 5 : tz_199680.bin (258129 bytes)
 6/ 6 : sdi_201728.bin (14684 bytes)
 7/ 7 : hyp_202752.bin (23677 bytes)
 8/ 8 : rpm_203776.bin (111265 bytes)
 9/ 9 : aboot_204800.bin (407367 bytes)
10/10 : sbl1bak_208896.bin (290373 bytes)
11/11 : pmicbak_210944.bin (11065 bytes)
12/12 : hypbak_211968.bin (23677 bytes)
13/13 : tzbak_212992.bin (258129 bytes)
14/14 : rpmbak_215040.bin (111265 bytes)
15/15 : abootbak_216064.bin (407367 bytes)
16/16 : sdibak_220160.bin (14684 bytes)
17/?? : limits (<empty>)
18/?? : apdp (<empty>)
19/?? : msadp (<empty>)
20/?? : dpo (<empty>)
21/?? : spare2 (<empty>)
22/?? : persistent (<empty>)
23/?? : devinfo (<empty>)
24/?? : spare3 (<empty>)
25/?? : misc (<empty>)
26/17 : persist_278528.bin (23385 bytes)
27/?? : modemst1 (<empty>)
28/?? : modemst2 (<empty>)
29/?? : fsg (<empty>)
30/?? : fsc (<empty>)
31/?? : ssd (<empty>)
32/?? : keystore (<empty>)
33/?? : DDR (<empty>)
34/18 : sec_360448.bin (2603 bytes)
35/?? : encrypt (<empty>)
36/?? : eksst (<empty>)
37/19 : rct_363520.bin (2317 bytes)
38/?? : spare4 (<empty>)
39/20 : laf_376832.bin (19533292 bytes)
40/21 : boot_475136.bin (16694149 bytes)
41/22 : recovery_557056.bin (17891387 bytes)
42/?? : drm (<empty>)
43/?? : sns (<empty>)
44/?? : mpt (<empty>)
45/23 : raw_resources_737280.bin (888299 bytes)
46/24 : raw_resourcesbak_745472.bin (888299 bytes)
47/25 : factory_753664.bin (2317 bytes)
48/?? : spare5 (<empty>)
49/?? : fota (<empty>)
50/?? : fau (<empty>)
51/26 : system_901120.bin (25371453 bytes)
51/27 : system_1165448.bin (60652649 bytes)
51/28 : system_1429456.bin (65098099 bytes)
51/29 : system_1689736.bin (2313 bytes)
51/30 : system_1693784.bin (52573309 bytes)
51/31 : system_1953744.bin (64109275 bytes)
51/32 : system_2214024.bin (2313 bytes)
51/33 : system_2218072.bin (75157338 bytes)
51/34 : system_2478032.bin (56945821 bytes)
51/35 : system_2738312.bin (2313 bytes)
51/36 : system_2742360.bin (68310797 bytes)
51/37 : system_3002320.bin (54648076 bytes)
51/38 : system_3262600.bin (2313 bytes)
51/39 : system_3266648.bin (59937725 bytes)
51/40 : system_3526608.bin (66799033 bytes)
51/41 : system_3788752.bin (61032997 bytes)
51/42 : system_4050896.bin (88105175 bytes)
51/43 : system_4313040.bin (57305742 bytes)
51/44 : system_4575184.bin (59805583 bytes)
51/45 : system_4837328.bin (53946948 bytes)
51/46 : system_5099472.bin (62892749 bytes)
51/47 : system_5361616.bin (82165315 bytes)
51/48 : system_5623760.bin (68205296 bytes)
51/49 : system_5885904.bin (60609918 bytes)
51/50 : system_6148048.bin (80451673 bytes)
51/51 : system_6410192.bin (73034607 bytes)
51/52 : system_6672336.bin (59097445 bytes)
51/53 : system_6934480.bin (61310637 bytes)
51/54 : system_7196624.bin (58278602 bytes)
51/55 : system_7456904.bin (2313 bytes)
51/56 : system_7460952.bin (55951601 bytes)
51/57 : system_7720912.bin (64319230 bytes)
51/58 : system_7981192.bin (2313 bytes)
51/59 : system_7985240.bin (66376379 bytes)
51/60 : system_8245200.bin (62336405 bytes)
51/61 : system_8507344.bin (26426046 bytes)
51/62 : system_8765440.bin (2314 bytes)
51/63 : system_9027584.bin (2314 bytes)
51/64 : system_9289728.bin (2314 bytes)
51/65 : system_9551872.bin (2317 bytes)
51/66 : system_9554936.bin (35634261 bytes)
52/?? : cache (<empty>)
53/?? : userdata (<empty>)
54/?? : grow (<empty>)
55/67 : BackupGPT_122141696.bin (5174 bytes)
$ undz -f kdzextracted/H90120j_00.dz -x
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
[+] Extracting system_8507344.bin to system_8507344.bin.chunk
[+] Extracting system_8765440.bin to system_8765440.bin.chunk
[+] Extracting system_9027584.bin to system_9027584.bin.chunk
[+] Extracting system_9289728.bin to system_9289728.bin.chunk
[+] Extracting system_9551872.bin to system_9551872.bin.chunk
[+] Extracting system_9554936.bin to system_9554936.bin.chunk
[+] Extracting BackupGPT_122141696.bin to BackupGPT_122141696.bin.chunk
$ rm dzextracted/system_[0-9]*[0-9].bin.chunk
$ undz -f kdzextracted/H90120j_00.dz -s 51
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
[+] Extracting system_8507344.bin to system.image
[+] Extracting system_8765440.bin to system.image
[+] Extracting system_9027584.bin to system.image
[+] Extracting system_9289728.bin to system.image
[+] Extracting system_9551872.bin to system.image
[+] Extracting system_9554936.bin to system.image
$ 

The theory was at this point you can modify out/system.image to your liking.
For this particular device (LG H901), system.image is an EXT4 filesystem.  Many
tools exist for modifying EXT4 filesystems and these should work fine.

The next step would be reconstructing the file.  There are three steps, turning
the files into chunks, merging them together into a DZ file, and then merging
everything back into a KDZ file.  The first step has some quirks.

"image2chunks.py" currently has 3 strategies for breaking image files into
chunks.  At of this writing the prefered strategy is to make use of ext2simg
from the Android image utilities.  This produces results that differ somewhat
from LG's images, but is believed to produce sane results.  The differences
have me wondering whether LG's images are either unsafe, or else relying on
special knowledge of the hardware (is the eMMC certain to give back zero blocks
for TRIMmed areas?).

The next two strategies are utilizing support for SEEK_DATA and SEEK_HOLE, or
probing for the presence of holes.  Operating System support for
SEEK_DATA/SEEK_HOLE is decent, though to my knowledge no versions of Windows
include this.  This seems a bit of a cheat since it is relying on knowledge of
which areas of the image haven't been written to.  Probing marks an awful lot
of areas as holes, which leaves me uncomfortable believing the results to be
sane.  As such I reccommend the first if available (ext2simg is known to work
for Linux, but I'm unsure Windows binaries are available).

WARNING: It has been found there is some additional unknown verification
mechanism in LGE's tools.  Due to this mechanism currently the generated KDZ
files haven't been shown to work.  There are some guesses as to where the
mechanism is, but as of now not enough is known to work around it.

$ image2chunks --ext4 dzextracted/system.image
[+] Compressing system.image to system_901120.bin (0 empty blocks)
[+] Compressing system.image to system_1163264.bin (8 empty blocks)
[+] Compressing system.image to system_1425408.bin (8 empty blocks)
[+] Compressing system.image to system_1687552.bin (8 empty blocks)
[+] Compressing system.image to system_1949696.bin (8 empty blocks)
[+] Compressing system.image to system_2211840.bin (8 empty blocks)
[+] Compressing system.image to system_2473984.bin (8 empty blocks)
[+] Compressing system.image to system_2736128.bin (8 empty blocks)
[+] Compressing system.image to system_2998272.bin (8 empty blocks)
[+] Compressing system.image to system_3260416.bin (8 empty blocks)
[+] Compressing system.image to system_3522560.bin (8 empty blocks)
[+] Compressing system.image to system_3784704.bin (8 empty blocks)
[+] Compressing system.image to system_4046848.bin (8 empty blocks)
[+] Compressing system.image to system_4308992.bin (8 empty blocks)
[+] Compressing system.image to system_4571136.bin (8 empty blocks)
[+] Compressing system.image to system_4833280.bin (8 empty blocks)
[+] Compressing system.image to system_5095424.bin (8 empty blocks)
[+] Compressing system.image to system_5357568.bin (8 empty blocks)
[+] Compressing system.image to system_5619712.bin (8 empty blocks)
[+] Compressing system.image to system_5881856.bin (8 empty blocks)
[+] Compressing system.image to system_6144000.bin (8 empty blocks)
[+] Compressing system.image to system_6406144.bin (8 empty blocks)
[+] Compressing system.image to system_6668288.bin (8 empty blocks)
[+] Compressing system.image to system_6930432.bin (8 empty blocks)
[+] Compressing system.image to system_7192576.bin (8 empty blocks)
[+] Compressing system.image to system_7454720.bin (8 empty blocks)
[+] Compressing system.image to system_7716864.bin (8 empty blocks)
[+] Compressing system.image to system_7979008.bin (8 empty blocks)
[+] Compressing system.image to system_8241152.bin (8 empty blocks)
[+] Compressing system.image to system_8503296.bin (150056 empty blocks)
[+] Compressing system.image to system_8765440.bin (258096 empty blocks)
[+] Compressing system.image to system_9027584.bin (258096 empty blocks)
[+] Compressing system.image to system_9289728.bin (258096 empty blocks)
[+] Compressing system.image to system_9551872.bin (8 empty blocks)
[+] done

$ mkdz -f kdzextracted/H90120j_00.dz -m
[+] Writing 60 chunks to H90120j_00.dz:

[+] Writing PrimaryGPT_0.bin.chunk to H90120j_00.dz (5711 bytes)
[+] Writing modem_16384.bin.chunk to H90120j_00.dz (42902812 bytes)
[+] Writing pmic_196608.bin.chunk to H90120j_00.dz (11577 bytes)
[+] Writing sbl1_197632.bin.chunk to H90120j_00.dz (290885 bytes)
[+] Writing tz_199680.bin.chunk to H90120j_00.dz (258641 bytes)
[+] Writing sdi_201728.bin.chunk to H90120j_00.dz (15196 bytes)
[+] Writing hyp_202752.bin.chunk to H90120j_00.dz (24189 bytes)
[+] Writing rpm_203776.bin.chunk to H90120j_00.dz (111777 bytes)
[+] Writing aboot_204800.bin.chunk to H90120j_00.dz (407879 bytes)
[+] Writing sbl1bak_208896.bin.chunk to H90120j_00.dz (290885 bytes)
[+] Writing pmicbak_210944.bin.chunk to H90120j_00.dz (11577 bytes)
[+] Writing hypbak_211968.bin.chunk to H90120j_00.dz (24189 bytes)
[+] Writing tzbak_212992.bin.chunk to H90120j_00.dz (258641 bytes)
[+] Writing rpmbak_215040.bin.chunk to H90120j_00.dz (111777 bytes)
[+] Writing abootbak_216064.bin.chunk to H90120j_00.dz (407879 bytes)
[+] Writing sdibak_220160.bin.chunk to H90120j_00.dz (15196 bytes)
[+] Writing persist_278528.bin.chunk to H90120j_00.dz (23897 bytes)
[+] Writing sec_360448.bin.chunk to H90120j_00.dz (3115 bytes)
[+] Writing rct_363520.bin.chunk to H90120j_00.dz (2829 bytes)
[+] Writing laf_376832.bin.chunk to H90120j_00.dz (19533804 bytes)
[+] Writing boot_475136.bin.chunk to H90120j_00.dz (16694661 bytes)
[+] Writing recovery_557056.bin.chunk to H90120j_00.dz (17891899 bytes)
[+] Writing raw_resources_737280.bin.chunk to H90120j_00.dz (888811 bytes)
[+] Writing raw_resourcesbak_745472.bin.chunk to H90120j_00.dz (888811 bytes)
[+] Writing factory_753664.bin.chunk to H90120j_00.dz (2829 bytes)
[+] Writing system_901120.bin.chunk to H90120j_00.dz (25368238 bytes)
[+] Writing system_1163264.bin.chunk to H90120j_00.dz (60662497 bytes)
[+] Writing system_1425408.bin.chunk to H90120j_00.dz (65117233 bytes)
[+] Writing system_1687552.bin.chunk to H90120j_00.dz (52590332 bytes)
[+] Writing system_1949696.bin.chunk to H90120j_00.dz (64116886 bytes)
[+] Writing system_2211840.bin.chunk to H90120j_00.dz (75176824 bytes)
[+] Writing system_2473984.bin.chunk to H90120j_00.dz (56952617 bytes)
[+] Writing system_2736128.bin.chunk to H90120j_00.dz (68318938 bytes)
[+] Writing system_2998272.bin.chunk to H90120j_00.dz (54652864 bytes)
[+] Writing system_3260416.bin.chunk to H90120j_00.dz (59959919 bytes)
[+] Writing system_3522560.bin.chunk to H90120j_00.dz (66803716 bytes)
[+] Writing system_3784704.bin.chunk to H90120j_00.dz (61048842 bytes)
[+] Writing system_4046848.bin.chunk to H90120j_00.dz (88113814 bytes)
[+] Writing system_4308992.bin.chunk to H90120j_00.dz (57314201 bytes)
[+] Writing system_4571136.bin.chunk to H90120j_00.dz (59818074 bytes)
[+] Writing system_4833280.bin.chunk to H90120j_00.dz (53953971 bytes)
[+] Writing system_5095424.bin.chunk to H90120j_00.dz (62896913 bytes)
[+] Writing system_5357568.bin.chunk to H90120j_00.dz (82167175 bytes)
[+] Writing system_5619712.bin.chunk to H90120j_00.dz (68191722 bytes)
[+] Writing system_5881856.bin.chunk to H90120j_00.dz (60612219 bytes)
[+] Writing system_6144000.bin.chunk to H90120j_00.dz (80457934 bytes)
[+] Writing system_6406144.bin.chunk to H90120j_00.dz (73042775 bytes)
[+] Writing system_6668288.bin.chunk to H90120j_00.dz (59107610 bytes)
[+] Writing system_6930432.bin.chunk to H90120j_00.dz (61329475 bytes)
[+] Writing system_7192576.bin.chunk to H90120j_00.dz (58290368 bytes)
[+] Writing system_7454720.bin.chunk to H90120j_00.dz (55970470 bytes)
[+] Writing system_7716864.bin.chunk to H90120j_00.dz (64312923 bytes)
[+] Writing system_7979008.bin.chunk to H90120j_00.dz (66396113 bytes)
[+] Writing system_8241152.bin.chunk to H90120j_00.dz (62351646 bytes)
[+] Writing system_8503296.bin.chunk to H90120j_00.dz (26438033 bytes)
[+] Writing system_8765440.bin.chunk to H90120j_00.dz (9577 bytes)
[+] Writing system_9027584.bin.chunk to H90120j_00.dz (9577 bytes)
[+] Writing system_9289728.bin.chunk to H90120j_00.dz (9577 bytes)
[+] Writing system_9551872.bin.chunk to H90120j_00.dz (35643326 bytes)
[+] Writing BackupGPT_122141696.bin.chunk to H90120j_00.dz (5686 bytes)
$ mkkdz -f myH901_20j.kdz -m
[+] Writing LGUP_c.dll to output file myH901_20j.kdz
[+] Writing LGUP_c.dylib to output file myH901_20j.kdz
[+] Writing H90120j_00.dz to output file myH901_20j.kdz

[+] Writing headers to myH901_20j.kdz
[+] Done!
$ 

At this point myH901_20j.kdz should be installable using LG's tools.  If the
image was unmodified, and image2chunks.py was used with its --sparse option,
it should be identical to the original file.  This second statement relies on
behavior of the OS and may not work precisely on all systems.  Exactly
identical files have only been shown on Linux with system.image being unpacked
onto a EXT4 FS (dzextracted being on EXT4).  EXT2/3 will also work if mounted
using the EXT4's backwards compatibility mode, rather than the native
implementation of EXT2/3.  Most other flavors of Unix should get sane output,
but not as likely to be identical.

There is a value in the chunk headers referred to as "trimCount" in the code,
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

WARNING: As of this writing it appears the fear of the unknowns was valid.
According to reports it appears there is an additional verification mechanism
which needs to be worked around.  At the moment I'm guessing "unknown1" (saved
in dzextracted/.dz.params) is a MD5 of some portion of the image.
Unfortunately without knowing which portion, it cannot be adjusted.  Similarly
"unknown3" could be a CRC-32 of the same area.  My fear is "unknown1" could be
a keyed hash at which point fixing is impossible unless we discover what/where
the key is.

One piece of good news is I'm pretty confident unpacking mostly works
correctly.  The one quirk is newer LGE devices (the G5) the DZ format is
somewhat modified and unpacking doesn't yet meet my expectations.


-------------------------------------------

Permission was granted to rerelease this software as long as attribution was
given.  This version is distributed under the terms of the GNU Public License
version 3.

-------------------------------------------

