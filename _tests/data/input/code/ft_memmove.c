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

void	*ft_memmove(void *dst, const void *src, size_t len)
{
	unsigned char		*d;
	const unsigned char	*s;

	d = dst;
	s = src;
	if (d == s)
		return (dst);
	if (d < s)
		return (ft_memcpy(d, s, len));
	else
	{
		while (len > 0)
		{
			*(d + (len - 1)) = *(unsigned char *)(s + (len - 1));
			len--;
		}
	}
	return (dst);
}

int main ()
{
	char src[] = "1234567890";
	char dest[50];

	ft_memmove(dest, src, 11);
	printf("copied string : %s\n", dest);
	return (0);
}
