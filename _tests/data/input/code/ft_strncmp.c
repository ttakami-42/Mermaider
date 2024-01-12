#include <stdio.h>

int	ft_strncmp(const char *s1, const char *s2, size_t len)
{
	while (len && *s1 && (*s1 == *s2))
	{
		s1++;
		s2++;
		len--;
	}
	if (len == 0)
		return (0);
	else
		return (*(unsigned char *) s1 - *(unsigned char *) s2);
}

int main()
{
	char *str1 = "abcdefghijk";
	char *str2 = "ghi";
	int i = ft_strncmp(str1, str2, 20);
	if (i > 0)
		printf("%s is greater than %s\n", str1, str2);
	else if (i < 0)
		printf("%s is less than %s\n", str1, str2);
	else
		printf("%s is equal to %s\n", str1, str2);
}
