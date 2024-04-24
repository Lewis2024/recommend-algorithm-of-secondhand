import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.beans.factory.annotation.Autowired;
import java.util.*;

@RestController
public class RecommendationController {
    @Autowired
    private RecommendationService recommendationService;

    @GetMapping("/recommendations")
    public List<Double> getRecommendations(@RequestParam String userId) {
        return recommendationService.getRecommendations(userId);
    }
}
