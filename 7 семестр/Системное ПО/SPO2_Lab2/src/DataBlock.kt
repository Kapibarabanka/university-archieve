import java.io.Serializable

class DataBlock : Serializable {
    var data = ByteArray(BLOCK_SIZE)
    init {
        fillWithBlanks(0 until BLOCK_SIZE)
    }

    fun writeData(input: String, offset: Int = 0) {
        for ((idx, i) in (offset until BLOCK_SIZE).withIndex()) {
            data[i] = input[idx].toByte()
            if (idx == input.length - 1)
                break
        }
    }

    fun fillWithBlanks(range: IntRange) {
        for (i in range) {
            data[i] = EMPTY_CHAR.toByte()
        }
    }
}