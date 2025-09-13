package com.businessanalysis.marketanalysis.repository;

import com.businessanalysis.marketanalysis.model.UserInput;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface UserInputRepository extends JpaRepository<UserInput, Long> {
    
    List<UserInput> findByLocation(String location);
    
    List<UserInput> findByBusinessInterest(String businessInterest);
    
    @Query("SELECT u FROM UserInput u WHERE u.capitalMin >= :minCapital AND u.capitalMax <= :maxCapital")
    List<UserInput> findByCapitalRange(@Param("minCapital") Double minCapital, 
                                      @Param("maxCapital") Double maxCapital);
    
    @Query("SELECT u FROM UserInput u WHERE u.location = :location AND u.businessInterest = :businessInterest")
    List<UserInput> findByLocationAndBusinessInterest(@Param("location") String location, 
                                                     @Param("businessInterest") String businessInterest);
}