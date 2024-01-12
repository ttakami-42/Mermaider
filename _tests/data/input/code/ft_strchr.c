#include <stdio.h>

char	*ft_strchr(const char *str, int c)
{
	while (*str != '\0')
	{
		if (*str == (const char)c)
			return ((char *)str);
		str++;
	}
	if ((const char)c == '\0')
		return ((char *)str);
	return (NULL);
}

int main()
{
	char *str = "1234567890";
	char c = '5';
	char *ptr = ft_strchr(str, c);

	printf("%s\n", ptr);
}
