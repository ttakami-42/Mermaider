#include <stdio.h>

void	*ft_memcpy(void *dst, const void *src, size_t len)
{
	unsigned char	*ptr;

	ptr = dst;
	if (dst == src)
		return (dst);
	while (len-- > 0)
		*ptr++ = *(unsigned char *)src++;
	return (dst);
}

int main()
{
	char *src = "1234567890";
	char dest[50];
	
	ft_memcpy(dest, src, 11);
	printf("copied string : %s\n", dest);
	return (0);
}
