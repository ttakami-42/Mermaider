#include <stdio.h>

static size_t	ft_strnlen(const char *str, size_t maxlen)
{
	size_t	i;

	i = 0;
	while (i < maxlen && str[i] != '\0')
		i++;
	return (i);
}

size_t	ft_strlen(const char *str)
{
	size_t	i;

	i = 0;
	while (str[i] != '\0')
		i++;
	return (i);
}

size_t	ft_strlcpy(char *dst, const char *src, size_t size)
{
	size_t	i;

	i = 0;
	if (size > 0)
	{
		while (src[i] != '\0' && i < (size - 1))
		{
			dst[i] = src[i];
			i++;
		}
		dst[i] = '\0';
	}
	return (ft_strlen(src));
}

size_t	ft_strlcat(char *dst, const char *src, size_t size)
{
	size_t	dst_len;

	dst_len = 0;
	if (size != 0)
		dst_len = ft_strnlen(dst, size);
	return (dst_len + ft_strlcpy(dst + dst_len, src, (size - dst_len)));
}

int main()
{
	char *src = "1234567890";
	char dst[50];
	int i = ft_strlcat(dst, src, 11);

	printf("[%s] is %d.\n", dst, i);
}
