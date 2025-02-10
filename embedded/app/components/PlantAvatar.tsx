import { Sprout, Leaf, Frown, Smile, type LucideIcon } from "lucide-react"

interface PlantAvatarProps {
  happiness: number
}

export default function PlantAvatar({ happiness }: PlantAvatarProps) {
  let MoodIcon: LucideIcon
  let color: string

  if (happiness < 30) {
    MoodIcon = Frown
    color = "text-red-500"
  } else if (happiness < 70) {
    MoodIcon = Sprout
    color = "text-yellow-500"
  } else {
    MoodIcon = Smile
    color = "text-green-500"
  }

  return (
    <div className="flex items-center justify-center space-x-4">
      <Leaf className="text-pink-400 w-24 h-24" />
      <MoodIcon className={`${color} w-24 h-24`} />
    </div>
  )
}

