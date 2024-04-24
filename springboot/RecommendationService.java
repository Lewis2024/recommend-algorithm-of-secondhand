import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;
import org.apache.commons.math3.stat.correlation.PearsonsCorrelation;
import java.util.*;

@Service
public class RecommendationService {
    @Autowired
    private UserMapper userMapper;

    public List<Double> getRecommendations(String currentUserId) {
        int totalNumberOfProducts = userMapper.getTotalNumberOfProducts();
        List<Integer> currentUserInteractionList = generateInteractionList(currentUserId, totalNumberOfProducts);
        List<List<Integer>> otherUsersInteractionList = generateAllUsersInteractionList(currentUserId, totalNumberOfProducts);

        PearsonsCorrelation correlation = new PearsonsCorrelation();
        double[] s = new double[totalNumberOfProducts];
        double[] R = new double[totalNumberOfProducts];
        for (List<Integer> list : otherUsersInteractionList) {
            double[] listArray = list.stream().mapToDouble(i -> i).toArray();
            double corr = correlation.correlation(currentUserInteractionList.stream().mapToDouble(i -> i).toArray(), listArray);
            for (int i = 0; i < totalNumberOfProducts; i++) {
                s[i] += corr;
                R[i] += (listArray[i] - Arrays.stream(listArray).average().orElse(0)) * corr;
            }
        }

        double meanI = currentUserInteractionList.stream().mapToInt(i -> i).average().orElse(0);
        List<Double> recommendations = new ArrayList<>();
        for (int i = 0; i < totalNumberOfProducts; i++) {
            recommendations.add(meanI + R[i] / Math.abs(s[i]));
        }

        return recommendations;
    }

    private List<Integer> generateInteractionList(String userId, int totalNumberOfProducts) {
        List<Integer> interactionList = new ArrayList<>(Collections.nCopies(totalNumberOfProducts, 0));
        List<Integer> collectRecords = userMapper.getCollectRecords(userId);
        List<Integer> purchaseRecords = userMapper.getPurchaseRecords(userId);

        for (Integer fid : collectRecords) {
            if (fid <= totalNumberOfProducts) {
                interactionList.set(fid - 1, 1);
            }
        }

        for (Integer orderId : purchaseRecords) {
            if (orderId <= totalNumberOfProducts) {
                interactionList.set(orderId - 1, interactionList.get(orderId - 1) == 1 ? 2 : 1);
            }
        }

        return interactionList;
    }

    private List<List<Integer>> generateAllUsersInteractionList(String currentUserId, int totalNumberOfProducts) {
        List<List<Integer>> allUsersInteractionList = new ArrayList<>();
        List<String> userIds = userMapper.getAllUserIds();

        for (String userId : userIds) {
            if (!userId.equals(currentUserId)) {
                allUsersInteractionList.add(generateInteractionList(userId, totalNumberOfProducts));
            }
        }

        return allUsersInteractionList;
    }
}
