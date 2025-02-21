// useMapData.ts
import { useState, useEffect, Dispatch, SetStateAction } from "react";
import { getObjects, getCategories } from "../services/mapServices";
import { Category, ObjectItem } from "@/utils/types";

function useMapData(date: Date|null, setStartDate: Dispatch<SetStateAction<Date>>) {
  const [objects, setObjects] = useState<ObjectItem[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const fetchData = async () => {
    try {
      const objectsData = await getObjects();
      const categoriesData = await getCategories();
      // Add categoryName to each object
      objectsData.forEach((obj) => {
        obj.categoryName = categoriesData.find(
          (cat) => cat.id === obj.categoryId
        )?.name;
      });
      setStartDate(new Date());
      setObjects(objectsData);
      setCategories(categoriesData);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return { objects, categories, date,refetchData: fetchData };
}

export default useMapData;
