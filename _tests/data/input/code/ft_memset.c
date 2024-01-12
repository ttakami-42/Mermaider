#include <stdio.h>

void	*ft_memset(void *dst, int val, size_t len)
{
	unsigned char	*ptr;

	ptr = dst;
	while (len-- > 0)
		*ptr++ = val;
	return (dst);
}

int main()
{
	char str[] = "1234567890";
	char *ptr = ft_memset(str, 'a', 5);

	printf("%s\n", ptr);
}
