package main

import (
	"flag"
	"math"
	"runtime"
	"strconv"
	"sync"
)

func sqrt(n float64) int {
	var y []float64
	for n >= 0 {
		y = append(y, n)
		n -= 1
	}
	for _, x := range y {
		// x = float64(x)
		// fmt.Print(x)
		math.Sqrt(x * (x - 1.0))
	}
	return 1
}

func ackerman(m, n int) int {
	if m == 0 {
		return n + 1
	} else if m > 0 && n == 0 {
		return ackerman(m-1, 1)
	}
	return ackerman(m-1, ackerman(m, n-1))
}

func main() {
	var wg sync.WaitGroup
	flag.Parse()
	args := flag.Args()
	f := args[0]
	procs, _ := strconv.Atoi(args[1])
	m, _ := strconv.Atoi(args[2])
	n, _ := strconv.Atoi(args[3])
	wg.Add(procs)
	for procs > 0 {
		go func() {
			runtime.LockOSThread()
			defer wg.Done()
			if f == "sqrt" {
				sqrt(float64((m*n)*m ^ 2))
			} else {
				ackerman(m, n)
			}
		}()
		procs -= 1
	}
	wg.Wait()
}
