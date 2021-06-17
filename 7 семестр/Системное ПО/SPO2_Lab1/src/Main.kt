const val PHYS_PAGES = 5
const val CLEAR_TIME = 10
const val TOTAL_TIME = 50
const val PROCESSES = 2

fun main(args: Array<String>){
    val os = Os()

    os.go()
}

val Boolean.int
    get() = if (this) 1 else 0

val Int.bool
    get() = this == 1