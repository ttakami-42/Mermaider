#include <stdarg.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdint.h>

size_t	ft_strlen(const char *str)
{
	size_t	i;

	i = 0;
	while (str[i] != '\0')
		i++;
	return (i);
}

static unsigned int	ft_count_ndigit(long num)
{
	unsigned int	count;

	count = 0;
	if (num <= 0)
	{
		num *= -1;
		count += 1;
	}
	while (num >= 1)
	{
		num /= 10;
		count++;
	}
	return (count);
}

char	*ft_itoa(int n)
{
	char			*result;
	unsigned int	digit;
	long			num;

	num = n;
	digit = ft_count_ndigit(n);
	result = malloc((digit + 1) * sizeof(char));
	if (!result)
		return (NULL);
	result[digit] = '\0';
	if (n == 0)
		result[0] = '0';
	if (n < 0)
	{
		result[0] = '-';
		num *= -1;
	}
	while (num > 0)
	{
		result[digit - 1] = num % 10 + '0';
		num = num / 10;
		digit--;
	}
	return (result);
}


char	*ft_uitoa_base(uintptr_t num, size_t rx, const char *base)
{
	ssize_t		digit;
	uintptr_t	tmp;
	char		*result;

	tmp = num;
	digit = 0;
	while (digit == 0 || tmp != 0)
	{
		tmp /= rx;
		digit++;
	}
	result = (char *)malloc((sizeof(char) * digit) + 1);
	if (!result)
		return (NULL);
	result[digit] = '\0';
	while (digit-- > 0)
	{
		result[digit] = base[num % rx];
		num /= rx;
	}
	return (result);
}

ssize_t	ft_put_char(int c)
{
	return (write(1, &c, 1));
}

static ssize_t	ft_put_string(char *str)
{
	ssize_t	len;

	if (!str)
		len = write(1, "(null)", 6);
	else
		len = write(1, str, ft_strlen(str));
	return (len);
}

static ssize_t	ft_put_int(int num)
{
	ssize_t	len;
	char	*str;

	str = ft_itoa(num);
	if (!str)
		return (-1);
	len = ft_put_string(str);
	free(str);
	return (len);
}

static ssize_t	ft_put_point(uintptr_t point, const char *base)
{
	ssize_t	len;
	char	*str;

	str = ft_uitoa_base(point, ft_strlen(base), base);
	if (!str)
		return (-1);
	len = ft_put_string("0x");
	if (len == -1)
	{
		free(str);
		return (-1);
	}
	len += ft_put_string(str);
	free(str);
	if (len == 1)
		return (-1);
	return (len);
}

static ssize_t	ft_put_uint_base(unsigned int num, const char *base)
{
	ssize_t	len;
	char	*str;

	str = ft_uitoa_base(num, ft_strlen(base), base);
	if (!str)
		return (-1);
	len = ft_put_string(str);
	free(str);
	return (len);
}

ssize_t	ft_put_sth(int c, va_list *args)
{
	va_list	temp;
	ssize_t	len;

	len = 0;
	va_copy(temp, *args);
	if (c == 'c')
		len = ft_put_char(va_arg(temp, int));
	else if (c == 's')
		len = ft_put_string(va_arg(temp, char *));
	else if (c == 'p')
		len = ft_put_point((uintptr_t)va_arg(temp, void *), "0123456789abcdef");
	else if (c == 'd' || c == 'i')
		len = ft_put_int(va_arg(temp, int));
	else if (c == 'u')
		len = ft_put_uint_base(va_arg(temp, unsigned int), "0123456789");
	else if (c == 'x')
		len = ft_put_uint_base(va_arg(temp, unsigned int), "0123456789abcdef");
	else if (c == 'X')
		len = ft_put_uint_base(va_arg(temp, unsigned int), "0123456789ABCDEF");
	else if (c == '%')
		len = ft_put_char(c);
	va_end(temp);
	return (len);
}

int	ft_printf(const char *fmt, ...)
{
	va_list	args;
	ssize_t	len;
	ssize_t	tmp;
	ssize_t	i;

	len = 0;
	i = -1;
	va_start(args, fmt);
	while (fmt[++i])
	{
		if (fmt[i] == '%' && fmt[i + 1])
			tmp = ft_put_sth(fmt[++i], &args);
		else
			tmp = ft_put_char(fmt[i]);
		if (tmp == -1)
			return (-1);
		len += tmp;
	}
	va_end(args);
	return ((int)len);
}

int main ()
{
	ft_printf("Hello %s!\n", "world");
}
