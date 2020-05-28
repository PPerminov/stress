#Stresstest

This one I'm using to multithreading stress for hard disk I/O and looped mem stress.

v.0.2.2

Variables:

-   **TIME_TO_RUN** Start time in "Hour:Minute:Second" format. To have an ability to start at one time if you need to stress from multiple containers for example. 0 == start immediately. Default **0**
-   **DEBUG** A little bit of debug Default **0**
-   **TYPE** Tests type: 1 == mem stress. 2 == hdd stress. 0 == 1 & 2. 3 == a lot of malloc() of C. Default **2**
-   **DISK_IO_PROCESSES** number of Python I/O processes. Default **1**
-   **MAXFILESIZE** Max file size. Default **20**
-   **WORK_PATH** Path to test. Default **/slow**
-   **READ_PRIORITY** Here is the number of read/write balance. From 1 to infinity. Bigger number == lesser possibility to start write process. Bigger number == more time needed to run full pressure. 1 == write only. Default **2**
-   **INITIAL_REMOVE** If one then will delete all files in **WORK_PATH** with name lenght of 128 chars. Otherways will use all 128 cars lenght files for test needs. **Default 1**
-   **STRESS_PROCESSES** Number of processes of mem stress. **Default 1**
-   **MAX_MEM** Maximum amount of mem that stress is allowed to allocate. **Default 60**
-   **MEM_INCREMENTER** Amount of mem that will be added with every iteration. Default **1**
-   **MEM** Starting ram amount in megabytes. Default **60**
-   **TIMEOUT** Timeout for one memstress iteration in seconds. Default **300**
-   **BRUTE_FORCE_AMOUNT** Amount of mem for brute_force malloc() in megabytes. Default **600**
-   **GENERATE_SOME_LOGS** Will just generate random logs as many as it can