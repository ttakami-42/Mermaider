#include <stdio.h>
#include <stdlib.h>

size_t	ft_strlen(const char *str)
{
	size_t	i;

	i = 0;
	while (str[i] != '\0')
		i++;
	return (i);
}

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

char	*ft_strdup(const char *src)
{
	char	*dst;
	size_t	len;

	len = ft_strlen(src) + 1;
	dst = (char *)malloc(sizeof(char) * len);
	if (!dst)
		return (NULL);
	ft_memcpy(dst, src, len);
	return (dst);
}

int main()
{
	char *src = "1234567890";
	char *dest;
	
	dest = ft_strdup(src);
	printf("copied string : %s\n", dest);
	return (0);
}
