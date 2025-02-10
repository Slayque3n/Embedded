"use client"

import { useState, useEffect } from "react"
import PlantAvatar from "./components/PlantAvatar"
import Logo from "./components/Logo"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface PlantStatus {
  moisture: number
  light: number
  temperature: number
  happiness: number
}

export default function Home() {
  const [plantStatus, setPlantStatus] = useState<PlantStatus>({
    moisture: 50,
    light: 50,
    temperature: 20,
    happiness: 50,
  })

  const fetchPlantStatus = async () => {
    try {
      const response = await fetch("/api/plant-status")
      const data = await response.json()
      setPlantStatus(data)
    } catch (error) {
      console.error("Error fetching plant status:", error)
    }
  }

  useEffect(() => {
    fetchPlantStatus()
  }, [])

  return (
    <main className="relative min-h-screen flex flex-col items-center justify-center p-24 bg-gradient-to-b from-pink-100 to-pink-200 overflow-hidden">
      {/* Decorative elements */}
      <div className="absolute top-0 left-0 w-full h-full pointer-events-none">
        <div className="absolute top-10 left-10 w-20 h-20 bg-pink-300 rounded-full opacity-50 animate-float"></div>
        <div className="absolute bottom-10 right-10 w-32 h-32 bg-green-200 rounded-full opacity-50 animate-float animation-delay-2000"></div>
        <div className="absolute top-1/4 right-1/4 w-16 h-16 bg-yellow-200 rounded-full opacity-50 animate-float animation-delay-1000"></div>
        <svg className="absolute bottom-0 left-0 w-full h-auto" viewBox="0 0 1440 320" preserveAspectRatio="none">
          <path
            fill="rgba(236, 72, 153, 0.1)"
            fillOpacity="1"
            d="M0,288L48,272C96,256,192,224,288,197.3C384,171,480,149,576,165.3C672,181,768,235,864,234.7C960,235,1056,181,1152,170.7C1248,160,1344,192,1392,208L1440,224L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
          ></path>
        </svg>
      </div>

      <div className="absolute top-4 left-4 z-20">
        <Logo />
      </div>

      <Card className="w-full max-w-md relative z-10 bg-white/80 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-center text-2xl font-bold text-pink-700">My Smart Plant</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col items-center space-y-8">
          <PlantAvatar happiness={plantStatus.happiness} />
          <div className="grid grid-cols-2 gap-6 w-full">
            <div className="text-center">
              <p className="font-semibold text-pink-600">Moisture</p>
              <p>{plantStatus.moisture}%</p>
            </div>
            <div className="text-center">
              <p className="font-semibold text-pink-600">Light</p>
              <p>{plantStatus.light}%</p>
            </div>
            <div className="text-center">
              <p className="font-semibold text-pink-600">Temperature</p>
              <p>{plantStatus.temperature}°C</p>
            </div>
            <div className="text-center">
              <p className="font-semibold text-pink-600">Happiness</p>
              <p>{plantStatus.happiness}%</p>
            </div>
          </div>
          <Button onClick={fetchPlantStatus} className="bg-pink-500 hover:bg-pink-600 text-white">
            Update Plant Status
          </Button>
        </CardContent>
      </Card>
    </main>
  )
}

