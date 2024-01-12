#include <stdio.h>
#include <limits.h>

int	ft_isdigit(int c)
{
	return ('0' <= c && c <= '9');
}

int	ft_isspace(int c)
{
	return ((9 <= c && c <= 13) || c == 32);
}

static int	ft_isoverflow(long *num, int is_neg, int c)
{
	long	cutoff;
	int		cutlim;

	if (is_neg)
	{
		cutoff = -(LONG_MIN / 10);
		cutlim = -(LONG_MIN % 10);
	}
	else
	{
		cutoff = LONG_MAX / 10;
		cutlim = LONG_MAX % 10;
	}
	if (*num > cutoff || (*num == cutoff && c > cutlim))
	{
		if (is_neg)
			*num = LONG_MIN;
		else
			*num = LONG_MAX;
		return (1);
	}
	return (0);
}

int	ft_atoi(const char *str)
{
	long	num;
	int		is_neg;

	num = 0;
	is_neg = 0;
	while (ft_isspace(*str))
		str++;
	if (*str == '-')
		is_neg = 1;
	if (*str == '-' || *str == '+')
		str++;
	while (ft_isdigit(*str))
	{
		if (ft_isoverflow(&num, is_neg, *str - '0'))
			break ;
		num = num * 10 + (*str++ - '0');
	}
	if (is_neg)
		return (-num);
	return (num);
}

int main()
{
	char *str = "1234567890";
	int i = ft_atoi(str);

	printf("%d\n", i);
}
