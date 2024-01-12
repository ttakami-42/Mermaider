#include <stdio.h>

int	ft_memcmp(const void *s1, const void *s2, size_t len)
{
	while (len-- > 0)
	{
		if (*(unsigned char *)s1 != *(unsigned char *)s2)
			return (*(unsigned char *)s1 - *(unsigned char *)s2);
		s1++;
		s2++;
	}
	return (0);
}

int main()
{
	char *str1 = "abcdefghijk";
	char *str2 = "ghi";
	int i = ft_memcmp(str1, str2, 20);

	if (i > 0)
		printf("%s is greater than %s\n", str1, str2);
	else if (i < 0)
		printf("%s is less than %s\n", str1, str2);
	else
		printf("%s is equal to %s\n", str1, str2);
}
