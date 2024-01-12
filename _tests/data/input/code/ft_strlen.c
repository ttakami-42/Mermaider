#include <stdio.h>

size_t	ft_strlen(const char *str)
{
	size_t	i;

	i = 0;
	while (str[i] != '\0')
		i++;
	return (i);
}

int main()
{
	char *str = "1234567890";
	int i = ft_strlen(str);

	printf("[%s] is %d.\n", str, i);
}
