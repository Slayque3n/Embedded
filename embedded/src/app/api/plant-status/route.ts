import { NextResponse } from "next/server"

export async function GET() {
  // Simulate a delay
  await new Promise((resolve) => setTimeout(resolve, 500))

  // Generate random values for the plant status
  const moisture = Math.floor(Math.random() * 100)
  const light = Math.floor(Math.random() * 100)
  const temperature = Math.floor(Math.random() * 15) + 15 // 15-30°C
  const happiness = Math.floor((moisture + light + (100 - Math.abs(temperature - 22) * 3)) / 3)

  return NextResponse.json({
    moisture,
    light,
    temperature,
    happiness: Math.min(100, Math.max(0, happiness)),
  })
}

