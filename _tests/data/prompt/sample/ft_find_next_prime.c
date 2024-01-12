#include <stdio.h>
#include <limits.h>

int	ft_is_prime(int nb)
{
	int	i;

	i = 2;
	while (nb % i != 0)
	{
		if (i > nb)
			break ;
		++i;
	}
	if (nb == i)
		return (1);
	return (0);
}

int	ft_find_next_prime(int nb)
{
	while (nb < INT_MAX)
	{
		if (ft_is_prime(nb))
			return (nb);
		++nb;
	}
}

int main ()
{
	printf("%d\n", ft_find_next_prime(15));
}
