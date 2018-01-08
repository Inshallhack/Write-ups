int main(int argc, char const *argv[])
{
	for (int v5 = 123456789; v5 <= 987654321; ++v5){
		for (int v6 = 123456789; v6 <= 987654321; ++v6){
			for (int v7 = 123456789; v7 <= 987654321; ++v7){
				for (int v8 = 123456789; v8 <= 987654321; ++v8){
					if (((v5 * v6 * v7 * v8 * ((v5 << 25) % 30) ) ^ (v6 >> 3) ) + v7 - v8 == 842675475){
						printf("%d %d %d %d\n", v5, v6, v7, v8);
						return 0;
					}
				}
			}
		}
	}
	return -1;
}