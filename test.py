import math
class Solution:
    def countPrimes(self, n: int) -> int:
        amount_primes = 0

        for i in range(2, n):
            if(self.isPrime(i)):
                amount_primes += 1
        
        return amount_primes

    def isPrime(self,n) -> bool:
        #Returns whether a value is prime or not
        for i in range(2, math.floor(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    

def main():
    answer = Solution()
    print(answer.countPrimes(5000000))

if __name__ == "__main__":
    main()
