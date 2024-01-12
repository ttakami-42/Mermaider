#include <stdio.h>

void	*ft_memchr(const void *s, int c, size_t len)
{
	while (len-- > 0)
	{
		if (*(unsigned char *)s == (unsigned char)c)
			return ((void *)s);
		s++;
	}
	return (NULL);
}

int main()
{
	char *str = "1234567890";
	char c = '5';
	char *ptr = ft_memchr(str, c, 5);

	printf("%s\n", ptr);
}
