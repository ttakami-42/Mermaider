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

char	*ft_substr(const char *str, unsigned int start, size_t len)
{
	char	*result;
	size_t	size;

	if (!str)
		return (NULL);
	size = ft_strlen(str);
	if (size <= start)
		size = 0;
	else
	{
		size = size - start;
		if (size > len)
			size = len;
	}
	result = malloc(sizeof(char) * (size + 1));
	if (!result)
		return (NULL);
	ft_memcpy(result, str + start, size);
	*(result + size) = '\0';
	return (result);
}

static size_t	ft_move_splitstart(char const *str, char c)
{
	size_t	count;

	count = 0;
	while (str[count] && str[count] == c)
		count++;
	return (count);
}

static size_t	ft_get_splitlen(char const *str, char c)
{
	size_t	count;

	count = 0;
	while (str[count] && str[count] != c)
		count++;
	return (count);
}

static size_t	ft_get_splittimes(char const *str, char c)
{
	size_t	elem;

	elem = 0;
	while (*str != '\0')
	{
		str += ft_move_splitstart(str, c);
		if (*str == '\0')
			break ;
		str += ft_get_splitlen(str, c);
		elem++;
	}
	return (elem);
}

static void	*ft_free_array(char **result)
{
	size_t	i;

	i = 0;
	while (result[i])
	{
		free(result[i]);
		i++;
	}
	free(result);
	return (NULL);
}

char	**ft_split(char const *str, char c)
{
	char	**result;
	size_t	split_len;
	size_t	split_count;
	size_t	result_i;

	if (!str)
		return (NULL);
	split_count = ft_get_splittimes(str, c);
	result = malloc(sizeof(char *) * (split_count + 1));
	if (!result)
		return (NULL);
	result_i = 0;
	while (result_i < split_count)
	{
		str += ft_move_splitstart(str, c);
		split_len = ft_get_splitlen(str, c);
		result[result_i] = ft_substr(str, 0, split_len);
		if (!result[result_i])
			return (ft_free_array(result));
		str += split_len;
		result_i++;
	}
	result[result_i] = NULL;
	return (result);
}

int main(void)
{
	char **result;
	char *str = "split  ||this|for|me|||||!|";
	char c = '|';

	result = ft_split(str, c);
	for (int i = 0; result[i]; i++)
		printf("%s\n", result[i]);
}
