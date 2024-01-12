#include <stdio.h>

char	*ft_strrchr(const char *str, int c)
{
	const char	*ptr;

	ptr = NULL;
	while (1)
	{
		if (*(str) == (const char)c)
			ptr = str;
		if (*(str) == '\0')
			break ;
		str++;
	}
	return ((char *)ptr);
}

int main()
{
	char *str = "1234567890";
	char c = '5';
	char *ptr = ft_strrchr(str, c);

	printf("%s\n", ptr);
}
