import { Leaf } from "lucide-react"

export default function Logo() {
  return (
    <div className="flex items-center space-x-2">
      <Leaf className="h-8 w-8 text-pink-600" />
      <span className="text-2xl font-bold text-pink-700">Plant Parenthood</span>
    </div>
  )
}

