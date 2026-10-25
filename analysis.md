# Zoe Eigenbrod
## Cryptology HW 4

# Problem 1

**1a.**
For Gen, given input $1^n$, a key is generated. For Mac, given $k$ and message $m$, it outputs a tag $t = x_\ell$. $x_0 = 0$. $x_i = F_k(x_{i-1} \oplus m_i)$ for $i = 1, \ldots, \ell$. For Vrfy, given $k$, $m$, and $t$, it will verify whether $t$ is valid for $m$ or not. It will output 0 if rejected and 1 if accepted.

**1b.**
The first difference is CBC-MAC creates a tag for verification, while CBC-mode encryption turns message to ciphertext. The second difference between CBC-MAC and CBC-mode encryption is how it handles output.  CBC-mode encryption will output every block, while CBC-MAC will only output the last block for tag. 


**1c.**
If $F$ is a secure PRF, CBC-MAC is secure when all the messages have the same length under the same key. It is no longer secure if the lengths are different because the attacker can forge a tag.

# Problem 2

**2a.**
For $m^*$, the chain values are

$$x_i^* = x_i \quad \text{for } 1 \le i \le \ell.$$

After the first $\ell$ blocks, the chain value is $x_\ell^* = t$. The next block is

$$x_{\ell+1}^* = F_k(t \oplus (m'_1 \oplus t)) = F_k(m'_1) = x'_1.$$

The remaining blocks are

$$x_{\ell+j}^* = x'_j \quad \text{for } 2 \le j \le \ell'.$$

The final chain value is $x_{\ell+\ell'}^* = x'_{\ell'} = t'$. This means

$$\boxed{\mathsf{Mac}_k(m^*) = t'}.$$

$m^*$ is different from $m$ because of the extra blocks. $m^*$ also differs from $m'$ because it contains the contents of $m$ plus the first modified block of $m'$.

**2b.**
The first query is $q_1 = M_1$, to get output tag $t_1$. The second query is $q_2 = (M_2 \oplus t_1) \| M_3 \| \cdots \| M_L$ to get output tag $t_2$. The first tag is $t_1 = F_k(M_1)$. By 2a with $m = q_1$ and $m' = q_2$, the forged message is

$$m^* = M_1 \| \big((M_2 \oplus t_1) \oplus t_1\big) \| M_3 \| \cdots \| M_L = M,$$

so $t_2$ is a valid tag on $M$. Neither the first or second query equals $M$ because $M$ has $L \ge 2$ blocks, while the first query has 1 block and the second query has $L-1$ blocks. The success probability is 1.

**2c.**
The attack fails because of the length. There needs to be exactly $\ell$ blocks. Part a has $m^*$ with $\ell + \ell'$ blocks. This is longer than the allowed $\ell$ length. Part b contains only one block in the first query and $L-1$ blocks for the second query, while the target $M$ has $L$ blocks. This does not match up with the required $\ell$ length. It is important that they fail so that an attacker cannot create a forgery.

**3b.**

Out of the 100 runs, all 100 resulted in successful forgeries. I included the first 5 runs below, but running demo.py will output all 100 runs.

```text
Target message: from=alice&to=mallory&amount=1000000&note=rent!!
Target hex: 66726f6d3d616c69636526746f3d6d616c6c6f727926616d6f756e743d31303030303030266e6f74653d72656e742121

run 1
query 1 message: 66726f6d3d616c69636526746f3d6d61
query 1 tag: 26d3caeeadab0ae3be68927d8c6d29c6
query 2 message: 4abfa59cd48d6b8ed11dfc09b15c19f630303030266e6f74653d72656e742121
query 2 tag: 455ffd1113b33936ece398132305dd96
forged tag: 455ffd1113b33936ece398132305dd96
oracle received target: False
accepted: True
successful forgery: True

run 2
query 1 message: 66726f6d3d616c69636526746f3d6d61
query 1 tag: ae53c8bbc11f410b24e53ab29d2e9c0e
query 2 message: c23fa7c9b83920664b9054c6a01fac3e30303030266e6f74653d72656e742121
query 2 tag: b76433dc390f335fc0df63361a0f8276
forged tag: b76433dc390f335fc0df63361a0f8276
oracle received target: False
accepted: True
successful forgery: True

run 3
query 1 message: 66726f6d3d616c69636526746f3d6d61
query 1 tag: cbb549ad8874f3bbf9e5ee74347a2b1e
query 2 message: a7d926dff15292d696908000094b1b2e30303030266e6f74653d72656e742121
query 2 tag: 6cd27314ef6843e3165c3b23e1576da0
forged tag: 6cd27314ef6843e3165c3b23e1576da0
oracle received target: False
accepted: True
successful forgery: True

run 4
query 1 message: 66726f6d3d616c69636526746f3d6d61
query 1 tag: 80ec9048b2e2503e770143fe898768c2
query 2 message: ec80ff3acbc4315318742d8ab4b658f230303030266e6f74653d72656e742121
query 2 tag: 339bbfa965ba34eac1ccaf2303fce7d7
forged tag: 339bbfa965ba34eac1ccaf2303fce7d7
oracle received target: False
accepted: True
successful forgery: True

run 5
query 1 message: 66726f6d3d616c69636526746f3d6d61
query 1 tag: 54bf4ed5e91055518b5a66f86c0ec25b
query 2 message: 38d321a79036343ce42f088c513ff26b30303030266e6f74653d72656e742121
query 2 tag: 2d0156c1fbd702e3493a06cc74919f6d
forged tag: 2d0156c1fbd702e3493a06cc74919f6d
oracle received target: False
accepted: True
successful forgery: True
```

**3c.**
```text
2 query forgery fails at query 1: oracle rejected a 1-block message (accepts only 3 blocks)
```