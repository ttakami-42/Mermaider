#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

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

void	*ft_calloc(size_t num, size_t size)
{
	void	*p;
	size_t	n;

	n = num * size;
	if (num == 0 || size == 0)
		n = 1;
	else if (size > SIZE_MAX / num)
		return (NULL);
	p = malloc(n);
	if (!p)
		return (NULL);
	ft_bzero(p, n);
	return (p);
}

int main()
{
	int *ptr = ft_calloc(5, sizeof(int));
	int i = 0;

	while (i < 5)
	{
		printf("%d\n", ptr[i]);
		i++;
	}
	return (0);
}
