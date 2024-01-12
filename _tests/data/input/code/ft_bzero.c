#include <stdio.h>

void	*ft_memset(void *dst, int val, size_t len)
{
	unsigned char	*ptr;

	ptr = dst;
	while (len-- > 0)
		*ptr++ = val;
	return (dst);
}

void	ft_bzero(void *s, size_t len)
{
	ft_memset(s, 0, len);
}

int main()
{
	char str[] = "1234567890";
	int i = 0;

	ft_bzero(str, 5);
	while (i < 10)
	{
		if (str[i] == '\0')
			printf("0\n");
		else
			printf("%c\n", str[i]);
		i++;
	}
}
