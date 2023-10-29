package main

import (
	"bufio"
	"fmt"
	"os"
)

func B() {
	in := bufio.NewReader(os.Stdin)
	out := bufio.NewWriter(os.Stdout)
	defer out.Flush()

	var s string
	_, _ = fmt.Fscan(in, &s)

	_, _ = fmt.Fprintln(out, string(getModifiedString([]byte(s))))
}

func getModifiedString(s []byte) []byte {
	yandex := []byte("Yandex")
	cup := []byte("Cup")
	yandexCostToMinInd := make(map[int]int)
	cupCostToMaxInd := make(map[int]int)
	for i := range s {
		if i+len(yandex) <= len(s) && len(yandexCostToMinInd) < 6 {
			yandexCost := getMakeStrCost(s[i:], yandex)
			if _, ok := yandexCostToMinInd[yandexCost]; !ok {
				yandexCostToMinInd[yandexCost] = i
			}
		}
		if i >= len(yandex) && i+len(cup) <= len(s) {
			cupCost := getMakeStrCost(s[i:], cup)
			cupCostToMaxInd[cupCost] = i
		}
	}

	yandexInd := 0
	cupInd := 0
	for cost := 0; cost <= len(yandex)+len(cup); cost++ {
		needToBreak := false
		maxYandexCost := min(len(yandex), cost)
		for yandexCost := 0; yandexCost <= maxYandexCost; yandexCost++ {
			cupCost := cost - yandexCost
			var ok bool
			yandexInd, ok = yandexCostToMinInd[yandexCost]
			if !ok {
				continue
			}
			cupInd, ok = cupCostToMaxInd[cupCost]
			if !ok {
				continue
			}
			if yandexInd+len(yandex) <= cupInd {
				needToBreak = true
				break
			}
		}
		if needToBreak {
			break
		}
	}

	for i := 0; i < len(yandex); i++ {
		s[yandexInd+i] = yandex[i]
	}
	for i := 0; i < len(cup); i++ {
		s[cupInd+i] = cup[i]
	}

	return s
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func getMakeStrCost(s, target []byte) int {
	res := 0
	for i := range target {
		if s[i] != target[i] {
			res += 1
		}
	}
	return res
}

func main() {
	B()
}
